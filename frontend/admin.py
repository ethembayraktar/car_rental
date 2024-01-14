from django.contrib import admin
from django.utils.translation import gettext_lazy as _

from frontend.models import Seo, Frontend


class SeoAdmin(admin.ModelAdmin):
    search_fields = ('url', 'slug', 'title')
    list_display = ('url', 'slug', 'title')
    model = Seo
    fieldsets = (
        (
            _("General Info"), {
                "fields": (
                    'url',
                    'slug',
                    'title',
                    'description',
                    'keywords',
                    'author',
                    'owner',
                    'copyright'
                )}),
        (
            _("GEO"), {
                "fields": (
                    'geo_position',
                    'geo_region',
                    'geo_placename',
                )}),
        (
            _("OG"), {
                "fields": (
                    'og_price_amount',
                    'og_price_currency',
                    'og_site_name',
                    'og_description',
                    'og_image',
                    'og_url',
                    'og_type',
                    'og_title',
                )}),

        (
            _("Twitter"), {
                "fields": (
                    'twitter_card',
                    'twitter_site',
                    'twitter_title',
                    'twitter_description',
                    'twitter_creator',
                    'twitter_image',
                    'twitter_data1',
                    'twitter_label1',
                    'twitter_data2',
                    'twitter_label2'
                )}),
        (
            _("Important People"),
            {
                "fields": (
                    "deleted_by",
                    "updated_by",
                    "created_by",
                )}),
        (
            _("Important Dates"),
            {
                "fields": (
                    "deleted_at",
                    "updated_at",
                    "created_at",
                )}),
    )
    readonly_fields = ('slug', 'deleted_at', 'updated_at', 'created_at')


class FrontendAdmin(admin.ModelAdmin):
    search_fields = ('id', 'slug', 'title', 'sub_title', 'short_text', 'text')
    list_display = ('id', "site_name", 'slug', 'title', 'sub_title')

    model = Frontend
    fieldsets = (
        (
            _("General Settings"), {
                "fields": (
                    "site_name",
                    "address",
                    "phone1",
                    "phone2",
                    "email1",
                    "email2",
                    "slug",
                    "title",
                    "sub_title",
                    "memnun_musteri",
                    "yol_yardim",
                    "hizmet",
                    "hizmet_noktasi",
                    "text",
                    "short_text")}),
        (
            _("Images & Videos"),
            {
                "fields": (
                    "panel_login_bg",
                    "ajax_loading",
                    "logo",
                    "favicon",
                    "add_video",
                    "image_add_video",
                    "contact_image",
                    "footer_image",
                    "image1",
                    "image2",
                    "is_active",
                    "is_deleted"
                )}),

        (
            _("Social Media Addresses"),
            {
                "fields": (
                    "linkedin",
                    "instagram",
                    "youtube",
                    "facebook",
                    "tiktok",
                    "twitter",
                )}),
        (
            _("Important People"),
            {
                "fields": (
                    "deleted_by",
                    "updated_by",
                    "created_by",
                )}),
        (
            _("Important Dates"),
            {
                "fields": (
                    "deleted_at",
                    "updated_at",
                    "created_at",
                )}),
    )
    readonly_fields = ('slug', 'deleted_at', 'updated_at', 'created_at')


admin.site.register(Seo, SeoAdmin)
admin.site.register(Frontend, FrontendAdmin)

