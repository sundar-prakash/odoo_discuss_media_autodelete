# Discuss Media Auto-Delete

Odoo 19 module to automatically clean up and delete Discuss channel media and attachments after a configurable retention period.

## Features
* Enable / disable the auto-cleanup from Settings.
* Set any custom retention period in days (e.g. 30, 60, 90...).
* A daily scheduled action (cron) checks and deletes attachments whose age exceeds the configured number of days.
* Only touches attachments that belong to Discuss channels (`res_model = 'discuss.channel'`) - nothing else in the system is affected (no Documents, no Chatter attachments on other records, no emails).
* Deletion is logged so you can audit what was removed and when.

## Configuration
To configure the auto-delete settings:
1. Ensure your user has **Administration / Settings** access rights.
2. Go to the **Settings** app in Odoo.
3. In the left sidebar, stay on **General Settings**.
4. Scroll down until you find the **Discuss Media Cleanup** section.
5. Check the box for **Auto-delete Discuss Files** and set your preferred retention days.

## Usage
**Note:** Deletion is permanent. Make sure your retention period is long enough for your organization's needs before enabling this in production.

## License
This project is licensed under the LGPL-3 License - see the [LICENSE](LICENSE) file for details.
