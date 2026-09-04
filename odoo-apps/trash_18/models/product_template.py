# -*- coding: utf-8 -*-
from odoo import models


class ProductTemplate(models.Model):
    """أول موديل بيستخدم السلة: المنتجات."""

    _name = 'product.template'
    _inherit = ['product.template', 'trash.mixin']
