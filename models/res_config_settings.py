from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    discuss_media_autodelete_enabled = fields.Boolean(
        string="Auto-delete Discuss Files",
        config_parameter="discuss_media_autodelete.enabled",
        help="When enabled, a daily job will permanently delete files/media "
             "shared in Discuss channels and direct messages once they are "
             "older than the configured number of days.",
    )
    discuss_media_autodelete_days = fields.Integer(
        string="Delete Files Older Than (days)",
        config_parameter="discuss_media_autodelete.days",
        default=60,
        help="Number of days to keep Discuss files/media before they are "
             "automatically deleted. Common values: 30, 60, 90.",
    )
    discuss_media_autodelete_only_media = fields.Boolean(
        string="Only Media Files (images, videos, audio)",
        config_parameter="discuss_media_autodelete.only_media",
        help="If checked, only image/video/audio files are auto-deleted; "
             "other file types (PDF, docs, etc.) shared in Discuss are kept. "
             "Leave unchecked to delete ALL file types shared in Discuss.",
    )

    @api.onchange("discuss_media_autodelete_days")
    def _onchange_discuss_media_autodelete_days(self):
        if self.discuss_media_autodelete_days and self.discuss_media_autodelete_days < 1:
            self.discuss_media_autodelete_days = 1
