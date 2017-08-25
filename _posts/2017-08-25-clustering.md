---
layout: post
title: Clustering the messages
---

I am continue with telling about the tasks I faced during the implementing of oVirt log analyzer.

## What should the user see?
One of the most important issues about the analyzer's invention is how to classify the level of messages' "importance". Even if you want to analyze logs of only several minutes time range, they might contain thousands of lines.  User should see only useful and important messages, while the others should be filtered. The first idea is to use some keywords in messages, for example "error" - meaning that the message could be important as there was something wrong. But what if you want to understand the reasons caused this error? They could be presented in chains of on first sight ordinary messages.

## How does it work
Different parts of oVirt system generates many logs. Each of them contain detailed information about itself and also an information related to other parts during their communication. The ideal way to implement log files analysis is to restore the scheme from all logs. I tried to do this before the start of the internship with very simple way (just linking only errors if they were followed by the increased number of errors). Of course there are too many difficulties to do this, and after implementing the parsing I decided to test another method.

## Message's features
Each message in the log file may be more or less useful when solving different tasks. For example, if you are searching for a reason of some error, you might want to examine all previous warnings, and if you want to make sure that the configuration of your system was correct, you need to see messages representing its structure. All in all, in theory all messages can me marked and classified according to their meaning. I suggested the following metrics:

- Including the <<danger>> words like error, warning, fail, etc.
- Including the user-defined words, like some ID or part of a message.
- Checking if the number of errors of warning increased after the current message compared to the previous within a time window.
- Some other important identifiers, for example flags for showing long operations or tasks, that are constructed previously.

I'd also like to share the method of solving another important task. This task is a first step of recognizing the content of the message: we need to clusterize all messages into groups where messages within each group will me similar. This stage is important because log files are generating by algorithms and basically consists of pre-defined messages with some differences. 

### Clustering messages
The first simple step to unify similar messages was to remove all different parts from them. Typical situation in such messages is placing a unique information in brackets or quotes. Simple general illustration:

	New message "Hello" was received (Anastasia)
	New message "Good bye" was received (Victoria)

Now most unique parts are filtered, but usually messages have more complex structure, for example, nested brackets. So I decided to compare the content of all messages with each other and construct a distance matrix.

#### Distance between messages
**Levenshtein distance** is a string metric for measuring the difference between two sequences. Informally, the Levenshtein distance between two words is the minimum number of single-character edits (insertions, deletions or substitutions) required to change one word into the other. ([Source](https://en.wikibooks.org/wiki/Algorithm_Implementation/Strings/Levenshtein_distance))
```python
def distance(a, b):
    "Calculates the Levenshtein distance between a and b."
    n, m = len(a), len(b)
    if n > m:
        # Make sure n <= m, to use O(min(n,m)) space
        a, b = b, a
        n, m = m, n

    current_row = range(n+1) # Keep current and previous row, not entire matrix
    for i in range(1, m+1):
        previous_row, current_row = current_row, [i]+[0]*n
        for j in range(1,n+1):
            add, delete, change = previous_row[j]+1, current_row[j-1]+1, previous_row[j-1]
            if a[j-1] != b[i-1]:
                change += 1
            current_row[j] = min(add, delete, change)

    return current_row[n]
```
I tried the implementation from [editdistance](https://pypi.python.org/pypi/editdistance). It works much more faster than other that I tried, but is still quite slow, especially for long strings. Then I limited the string line and the speed become acceptable for our task.

OK, now we have a matrix, where small numbers represents a small amount of symbols to be changed/removed to make strings equal. Of course it highly depends on the string line, so the result was normalized on the full length of the string. The next step is to create groups of nearest neighbors from the known distances. The difficulties hides in the fact that we don't know, how many clusters there will be. So, I found the solution to use the only algorithm from `scikit-learn` that works without knowing the number of clusters.

#### Clustering
**DBSCAN** - Density-Based Spatial Clustering of Applications with Noise. Finds core samples of high density and expands clusters from them. Good for data which contains clusters of similar density. ([Source](http://scikit-learn.org/stable/modules/generated/sklearn.cluster.DBSCAN.html))

It may be more demanding on data compared to the KNN (for example), but works very fast and gives an informative result. Messages that didn't receive a cluster got a -1 marker (algorithm considered them a noise), but in our interpretation they have a unique content.

The problem was is the fact that a Levenshtein distance does not give a preference to an order of words. This means that in messages have similar tail but different beginning may go to one cluster. But in our task this situation is not typical: usually the informative part of message is located in the beginning, ant other long unique different indicators are placed at the end. For example, if you are debugging your program and need to check the value of some variable, most likely you will write ```print('my_count =', count)```. Thus, messages with different beginning was penalized, and vise versa, distance between messages with similar beginnings was reduced.

*Make it simpler*
As a result, I had to make the algorithm faster, and I tested the more simple way of clustering, and then left it due to acceptable accuracy. This is the way of placing each message on a cluster named by its first two words, and works fine for our task.

## Conclusion
The implementing of messages' clustering allows me to add the following features for messages:

- Frequency (size of the cluster)
- Does messages in the cluster differ by particular words, for example, IDs
- The coverage of the message of the whole log file and timeline

At the moment I am improving the details of the analyzer's implementation and testing these features. The next post most likely will be about creating the interface. Thanks for reading :)