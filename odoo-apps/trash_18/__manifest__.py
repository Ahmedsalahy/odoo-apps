# -*- coding: utf-8 -*-
{
    'name': 'سلة المحذوفات (Trash Bin)',
    'version': '18.0.1.0.0',
    'summary': 'حذف مؤقت (Soft Delete) بدل الحذف المباشر - يحتفظ بالسجلات 30 يوم قبل الحذف النهائي التلقائي',
    'description': """
سلة المحذوفات - Trash Bin
==========================
بدل حذف أي سجل مباشرة من قاعدة البيانات:

- السجل بينقل لـ "سلة المحذوفات" (active = False) مع تسجيل تاريخ الحذف.
- المستخدم يقدر يسترجعه في أي وقت قبل ما تنتهي المهلة.
- بعد 30 يوم، Scheduled Action (cron) بيحذفه نهائياً تلقائي.

النسخة الحالية مطبقة على المنتجات (product.template) كنقطة بداية،
والبنية (trash.mixin) مصممة تتوسع على أي موديل تاني بسهولة
(عملاء، فواتير، ...) من غير تكرار الكود.
    """,
    'category': 'Extra Tools',
    'author': 'Ahmed Salah',
    'license': 'LGPL-3',
    'depends': ['product'],
    'data': [
        'security/ir.model.access.csv',
        'views/trash_views.xml',
        'data/ir_cron.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'trash_bin/static/src/scss/trash_kanban.scss',
        ],
    },
    'installable': True,
    'application': False,
    'auto_install': False,
}
