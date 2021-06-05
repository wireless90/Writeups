# WhatsMyIntent

Install the given [apk](https://github.com/wireless90/AndroidInternalsCTF/tree/main/WhatsMyIntent).

- Your task is to send an intent with action "dart_ctf". 
- Pull the flag from the returned intent. 
- Do not reverse the apk.


So what we need to do is to send an intent with action `dart_ctf`.

First lets create a new android application.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/p5pgkizs50f2dzev2kah.png)

Click `Create New Project`
 
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/jbj3gq0qtluarhfhi9bp.png)

Click `Empty Activity` 


![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ykd97bdybgzr7z8wa454.png)

Ensure its a `Java` based project.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/zurk62ti3egvojobugfi.png)

Lets create a new Intent under the `onCreate` function. We can see that it accepts a string, `action`.


Following that, we are going to call `startActivityForResult(intent, requestCode:2);`

This basically tries to start that activity and expects a result. As multiple activities can be started, we have added a `requestCode` to uniquely identify the activity result that we want. I just gave an arbitary number, `2`.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/id65ijbn9fghxvb9mmj1.png)
 
The above is how your code should now look like.
  

Now let's try running the app. This is what I get in my emulator.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/r7wtx43dx6au465trnuc.png)
 
The reason is because I have not installed the given apk into the emulator yet. Simply drag and drop it into the emulator to install the vulnerable `.apk` package. Once installed, run your application again.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/1jsu9pvi9hy9z7sxo58q.png)
 
Great! Our application has successfully started an activity using the intent. But we have not configured the code to process the result.

In order to do this, I override the onActivityResult callback.
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/j96vqkyexllmw4znv571.png)
 
Basically, we check our request code if equals to the one configured, `2`, then extract out the dictionary keys. For each key, we print out to logcat the value. And we have got the flag!
