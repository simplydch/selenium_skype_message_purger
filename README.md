## Delete all messages from Skype.

Microsoft, in their wisdom, don’t allow you to mass delete chats.  In my case this meant that syncing took a long time whenever I logged in.  I also don’t need or want records from 8+ years ago.
This is a python script I wrote using Selenium to automate the process.  This was essentially only used once so it is far from polished.  However, I’m making it available as a starting point for anyone wishing to do something similar.   

The script deletes chats with individuals, and clears group chats, that occurred before a certain date, defaulting to 1 year ago.  It can also leave group chats.   It is likely that the script will need to be run multiple times and the settings altered to complete cleaning.

If anyone is using this script I'm happy to answer questions and try to help with issues if I can, so please don't heistate to get in touch.

**Please Note:  I take no responsibility for this script not working, or behaving in unexpected ways.  I also make no claims that this data is removed from Microsoft’s, or anyone else’s, servers.  Deletion and chat clearing/leaving is carried out in the same way as if you were to do this manually.  You should read Microsoft’s documentation to establish what these methods do, and do not do, prior to proceeding.**
