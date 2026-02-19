# Doc

Thank you for using the tag-logger package !

This log module is meant to be as little and simple as possible, and to work on every project you want it on.

Feel free to modify the code depending on the uses, and if you think somethin misses or might be improved, please tell me on the github page of the project.

## To use it : 
the module is built to allow only one hidden instance of the Log object, so you don't have to instanciate the Log object.

To call the module :

    from taggedLog.log import Log

To open the log :

    Log.start_log(...)

then you can use the methods :

    Log.info(...) which write an information in the log
    Log.warning(...) which write a warning in the log
    Log.error(...) which write an error in the log

Finally, close your log at the end of your program :

    Log.close_log()

