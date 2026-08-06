{
    "name": "Discuss Media Auto-Delete",
    "version": "19.0.1.0.0",
    "summary": "Automatically delete Discuss chat/channel media & file attachments after a configurable number of days.",
    "description": """
Discuss Media Auto-Delete
==========================
Adds a simple, configurable way to automatically clean up files/media shared
inside Odoo Discuss (channels and direct messages) after a chosen retention
period (e.g. 30, 60, or any custom number of days).

Features
--------
* Enable / disable the auto-cleanup from Settings.
* Set any custom retention period in days (e.g. 30, 60, 90...).
* A daily scheduled action (cron) checks and deletes attachments whose
  age exceeds the configured number of days.
* Only touches attachments that belong to Discuss channels
  (res_model = 'discuss.channel') - nothing else in the system is affected
  (no Documents, no Chatter attachments on other records, no emails).
* Deletion is logged so you can audit what was removed and when.

Note: deletion is permanent. Make sure your retention period is long enough
for your organisation's needs before enabling this in production.
""",
    "category": "Discuss",
    "author": "Sundar Prakash, Odoo Community Association (OCA)",
    "website": "https://github.com/sundar-prakash",
    "license": "LGPL-3",
    "depends": ["mail", "base_setup"],
    "data": [
        "data/ir_cron_data.xml",
        "views/res_config_settings_views.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
}
