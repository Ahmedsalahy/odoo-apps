# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import api, fields, models

# مدة الاحتفاظ بالسجل في السلة قبل الحذف النهائي (بالأيام)
TRASH_RETENTION_DAYS = 30


class TrashMixin(models.AbstractModel):
    """Mixin عام لإضافة سلة محذوفات (Soft Delete) لأي موديل.

    أي موديل عايز يستخدم السلة، يورث منه زي كده:

        class ProductTemplate(models.Model):
            _name = 'product.template'
            _inherit = ['product.template', 'trash.mixin']

    الموديل المستهدف لازم يكون عنده حقل `active` أصلاً (موديلات أودو
    الأساسية غالباً عندها ده جاهز).
    """

    _name = 'trash.mixin'
    _description = 'Trash Mixin - دعم الحذف المؤقت'

    deleted_at = fields.Datetime(
        string='تاريخ النقل للسلة',
        readonly=True,
        copy=False,
    )
    is_trashed = fields.Boolean(
        string='في السلة',
        compute='_compute_is_trashed',
        store=True,
    )
    days_remaining = fields.Integer(
        string='الأيام المتبقية',
        compute='_compute_days_remaining',
    )

    @api.depends('active', 'deleted_at')
    def _compute_is_trashed(self):
        for rec in self:
            rec.is_trashed = (not rec.active) and bool(rec.deleted_at)

    @api.depends('deleted_at')
    def _compute_days_remaining(self):
        now = fields.Datetime.now()
        for rec in self:
            if rec.deleted_at:
                deadline = rec.deleted_at + timedelta(days=TRASH_RETENTION_DAYS)
                rec.days_remaining = max((deadline - now).days, 0)
            else:
                rec.days_remaining = TRASH_RETENTION_DAYS

    def action_move_to_trash(self):
        """ينقل السجل(ات) للسلة بدل حذفها فعلياً."""
        self.write({
            'active': False,
            'deleted_at': fields.Datetime.now(),
        })

    def action_restore_from_trash(self):
        """يسترجع السجل(ات) من السلة."""
        self.write({
            'active': True,
            'deleted_at': False,
        })

    def unlink(self):
        """أي محاولة حذف عادية (من الواجهة أو كود تاني) بتتحول لنقل
        للسلة، إلا لو الاستدعاء جاي من الـ cron نفسه (force_delete)."""
        if self.env.context.get('force_delete'):
            return super(TrashMixin, self).unlink()
        self.action_move_to_trash()
        return True

    @api.model
    def _cron_purge_trash(self, days=TRASH_RETENTION_DAYS):
        """تشغّلها Scheduled Action يومياً: بتحذف نهائياً أي سجل
        عدّى على نقله للسلة أكتر من `days` يوم."""
        cutoff = fields.Datetime.now() - timedelta(days=days)
        domain = [
            ('active', '=', False),
            ('deleted_at', '!=', False),
            ('deleted_at', '<=', cutoff),
        ]
        records = self.with_context(active_test=False).search(domain)
        if records:
            records.with_context(force_delete=True).unlink()
        return True
