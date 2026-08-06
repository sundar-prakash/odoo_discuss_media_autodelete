import logging
from datetime import timedelta

from odoo import api, fields, models

_logger = logging.getLogger(__name__)

# Mimetype prefixes considered "media" when the admin restricts cleanup
# to media-only files.
MEDIA_MIMETYPE_PREFIXES = ("image/", "video/", "audio/")


class IrAttachment(models.Model):
    _inherit = "ir.attachment"

    @api.model
    def _cron_autodelete_discuss_media(self):
        """Delete Discuss (channel/DM) attachments older than the
        configured retention period. Runs once a day via ir.cron.

        Only attachments whose res_model is 'discuss.channel' are ever
        touched, so attachments in other apps (Documents, Chatter on
        other records, emails, etc.) are never affected.
        """
        icp = self.env["ir.config_parameter"].sudo()

        enabled = icp.get_param("discuss_media_autodelete.enabled")
        if not enabled or enabled in ("False", "0", "false"):
            _logger.info("Discuss media auto-delete: disabled, skipping.")
            return

        try:
            days = int(icp.get_param("discuss_media_autodelete.days", default="60"))
        except (TypeError, ValueError):
            days = 60

        if days < 1:
            _logger.warning(
                "Discuss media auto-delete: invalid retention of %s day(s), skipping.",
                days,
            )
            return

        only_media = icp.get_param("discuss_media_autodelete.only_media")
        only_media = bool(only_media) and only_media not in ("False", "0", "false")

        cutoff_date = fields.Datetime.now() - timedelta(days=days)

        domain = [
            ("res_model", "=", "discuss.channel"),
            ("create_date", "<", cutoff_date),
        ]

        if only_media:
            mime_domain = []
            for prefix in MEDIA_MIMETYPE_PREFIXES:
                mime_domain.append(("mimetype", "=like", f"{prefix}%"))
            # OR the mimetype conditions together: ['|', '|', cond1, cond2, cond3]
            or_operators = ["|"] * (len(mime_domain) - 1)
            domain += or_operators + mime_domain

        attachments = self.sudo().search(domain)
        count = len(attachments)

        if not count:
            _logger.info(
                "Discuss media auto-delete: no attachments older than %s day(s) found.",
                days,
            )
            return

        _logger.info(
            "Discuss media auto-delete: deleting %s attachment(s) older than %s day(s) "
            "(only_media=%s).",
            count,
            days,
            only_media,
        )

        # Log names/ids before deletion for auditability, then remove them.
        for att in attachments:
            _logger.info(
                "Discuss media auto-delete: removing attachment id=%s name=%r "
                "channel_id=%s created=%s",
                att.id,
                att.name,
                att.res_id,
                att.create_date,
            )

        attachments.unlink()
