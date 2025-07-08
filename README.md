# Dictionary Graph
 This is a personal project in progress done out of curiosity. My plan is as follows:

 - Create a graph where every node is a word in the English dictionary
 - For each word on the graph, parse its definition into separate words
 - Connect every word to every other word contained in its own definition in a directed graph
 - Print a full graph of the dictionary

 Challenges: The dictionary I'm using contains over 100,000 words, each with definitions containing a range of one to a few dozen words. Most graphing tools will not be able to handle these numbers, and on top of serious optimization techinques, I may be forced to use a stronger computer to produce a final render.

 Goals: My goal is to find any patterns that emerge. There will be obvious ones, like the words "the", "and" and "a" being used in most definitions, but there may be other patterns that can give insight into the way decriptive language is used and even the way a dictionary is written.

Dictionary being used: Webster's Unabridged English Dictionary, found [here](https://github.com/matthewreagan/WebstersEnglishDictionary)

See requirements.txt for Python libraries used. Also using graph-tool.