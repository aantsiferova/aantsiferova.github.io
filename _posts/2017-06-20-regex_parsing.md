---
layout: post
title: Parsing text files with different formats
---
## The problem
The first stage of my work was to study how to read and recognize the content of different logs. I faced the situation when each part of the system has its own log format, and different versions may have slightly different formats:

	...
	2010-10-10 12:10:10,000 Warning [Some information] Message text 
	...
	Info::2010-10-10 12:10:10,000::(Some index)::[Some information] Message text (Some other code)
	...

I had several ideas about solving this task, and I'd like to share the results. We discussed two opportunities for recognizing different formats:


- read a file line-by-line and collect the repeated information in the lines, that represents the format. Separators, their
number and order would make the template for a log file line

- define a template manually for each format. This method assumes the user to add a new template if a new format appears to be analyzed, but the advantage is in saving time with no need to pre-read each log to construct the format template.

To avoid unexpected difficulties I've implemented the second approach and left the possibility to create an automatic template-building. 

## Simple solution
I used regular expression to define the file template. There are named fields with possible characters and separators in the templates, and all these constraints I've received after testing them on different log files that I have. On this stage on-line regular expression editor [Pythex](http://pythex.org) helped me a lot. After I have received a templates that matches only "their" formats, I've placed them in order from the most detailed (with many constrains) to the most common. I would spend a couple of days on this task, if there were no other difficulties.

## Facing difficulties
Since I analyze the log files, I can expect that each message would match the template of the format (no). So some lines suddenly does not match the template. We want to save as much information as we can, so it is better to parse them somehow of at least save the raw line. I list some of the examples when a line differs from the log file format:

#### *Disappering of date and time*
	...
	2010-10-10 12:10:10,000 Warning [Some information] Message text 
	Warning: some warning text
	2010-10-10 12:10:10,500 Info [Some information] Message text 
	...

I found out that not all log file lines include a date+time label. For example, some system messages, that could appear in any time between the previous and following log messages. The idea of processing such cases is in copying the date and time from the previous message and noticing it in the text of the parsed line. So if the date and tine was not detected in the log line, the line is sawed in a raw format and required fields are copied from the previous message. But even if the date+time is found it doesn't mean that the line will be matched.

#### *Disappering of date and time and it's appearing on the other place in the line*
	...
	2010-10-10 12:10:10,000 Warning [Some information] Message text 
	Warning: some warning text about 2010-05-24 18:30:16,400 date and time action
	2010-10-10 12:10:10,500 Info [Some information] Message text 
	...

We can found a date+time in a log line, but it is not located in the defined place for date times and just represents some other date+time in the message that is not related to the time of the line was written to the log file. All we can do is to try to match full line with the file format template and handle the exception, which would tell us about the wrong location of the date+time. The processing of this case also involves copying information from the previous message.

#### *One of the line fields includes `\n`*
	...
	2010-10-10 12:10:10,000 Warning [Some information] Message text 
	and it's continuation
	and more continuation
	and ending

	2010-10-10 12:10:10,500 Info [Some information] Message text 
	...

The most simple case is when the last line field become miltiline (common example -- Tracebacks). Then the line will match the template as on this step we don't know anything about the next line and it's relation to the current line. So if we read the line and parse it, and then found out that the next line does not match the template, we should concatenate it with the previous line, and do it until we read the "normal" matched line. This means that we should store the line until we make sure that we've read the full message. 

The more complex case is when the non-last field become multiline and moves the template-required fields of the message to another line.

	...
	2010-10-10 12:10:10,000 Warning [Some information] Message text 
	and it's continuation
	and (Some other code)

	2010-10-10 12:10:10,500 Info [Some information] Message text (Some other code)
	...

What do we see in this situation? The first line conclude the date+time, but does not match the template -- the explanation coincides the second case, but represents the other situation that can be solved. The idea is again to concatenate the lines until we reach the "normal" line, and then try to match the constructed line to the template. If there were lost fields, they will be found, and if the situation was about disappeared date+time, we will do the instructions from that case.

#### *Combination of several exceptions*
	...
	2010-10-10 12:10:10,000 Warning [Some information] Message text 
	and it's continuation
	and more continuation about 2010-05-24 18:30:16,400 date and time action
	and ending
	and (Some other code)

	Warning: some warning message
	2010-10-10 12:10:10,500 Info [Some information] Message text (Some other code)
	...

Of course during solving all the described non-standard situations I have been searching for their combinations and tested the implemented algorithm for them. One of the features of the parsing algorithm is in the constrains that the user could impose to it. For example, he or she could provide a date and time range in which the log messages are to be showed or define a particular keyword that should be a part of a message. So the analyzer do not have to process and store all rows, only those that correspond to conditions. And we have to check the conditions after we parse the whole message, because the found date+time could not relate to the message appearance, and the keywords could be located on the non-first line of the message, if it contains `\n`.

## Conclusion
The process of solving this problem was interesting and unusual for me. During scientific work and studies it turns out that you have a tiny bit of standardized data over which you need to write a lot of different things. But in is the case you have 100 lines of algorithm and you improve and modify them because every time there appears a new case, Which must be taken into account. The next stage promises to be more familiar to me and I will do my best and hope to meet expectations for the result.