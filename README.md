# ScheduleBot
Discord bot that scrapes the timeedit page for class schedules.

Description
----

<p> Schedulebot is a program for a Discord Bot that navigates the TimeEdit webpage and searches for weekly schedules and posts them on
  Discord either via a message command or on channel id's at a set time. </p>
  

      
Dependencies
-----

- [Selenium](https://github.com/SeleniumHQ/selenium)
    Used to navigate and search the TimeEdit page and get the raw page text.
- [Discord.py](https://github.com/Rapptz/discord.py)
    Used to communicate and interact with the Discord API - sadly it seems work has stopped on the project.
- [Pytz](https://github.com/stub42/pytz)
    A wonderful module that lets you enter and use timezones in an easy way - Just used for the update loop
