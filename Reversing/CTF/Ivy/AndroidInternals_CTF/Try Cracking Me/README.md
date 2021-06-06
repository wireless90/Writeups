# Try Cracking Me

My write up is also available at [dev.to/wireless90](https://dev.to/wireless90/try-cracking-me-android-internals-ctf-ex2-4ohl)


Get the [apk](https://github.com/wireless90/AndroidInternalsCTF/blob/main/Try%20Cracking%20Me/app-debug.apk) here.

Firstly, I fired up my android emulator and installed the `app-debug.apk`. Then I opened the app.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/2pfukburhwqee5f3qt8u.png)
 
It seems that the application is a flag checker. I need to enter the flag and it would tell me if it is correct.

Since the instructions did not bar me from decompiling the `apk`, I proceeded to install `jadx`, a dex to java decompiler.

```sh
$ sudo apt install jadx
$ sudo jadx-gui `pwd`/app-debug.apk
```

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/y7xvwq0ndz360pn9vpzo.png)

We have now decompiled the dex code into java and we have a nice GUI to browse through the files.

Lets take a look at the `AndroidManifest.xml`.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/cs4irg62erf31uw6aya4.png)

It says the location of the `Main Activity`. Lets open it up.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/5y6zs2h7w0jrsppb8osv.png)
 
Focus on the function `onTextChanged`.

```java
public void onTextChanged(CharSequence charSequence, int i, int i1, int i2) 
{
	if (charSequence.length() < 3) {
		view.setText(R.string.nc);
		return;
	}
	String txt = charSequence.toString();
	String str = "dart";
	if (txt.indexOf(str) == 0) {
		try {
			int val = Integer.parseInt(txt.substring(str.length()));
			if (val % 2 < 1) {
				int val2 = val >> 1;
				if (val2 > 700) {
					view.setText(R.string.nc);
					return;
				}
				int val3 = val2 * 31;
				if (val3 % 11 == 0 && val3 % 53 == 0) {
					view.setText(R.string.cr);
					return;
				}
			}
		} catch (NumberFormatException e) {
		}
	}
	view.setText(R.string.nc);
}
```
Let's break it down.

At the line,
```java
if (txt.indexOf(str) == 0) {
```
, we can see that it checks if the string starts with `dart`.
So we know that the string starts with `dart`.

Following that the line
```java
Integer.parseInt(txt.substring(str.length()));
```
, shows that the rest of the string following `dart` is actually an integer.

```java
if (val % 2 < 1)
```
, shows that the integer must be divisible by 2.

```java
int val2 = val >> 1;
```
, a right shift by 1 operator was done which divides the number by 2.

```java
if (val2 > 700) {
     view.setText(R.string.nc);
     return;
}
```
If the resulting operation is greater than `700`, it prints a message. This might be a wrong control flow path and might not lead us to the flag. But lets try `dart1422`, where `1422` is both divisible by 2, and the result would be greater than 700.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/jbun8fwm07zlv5testfc.png)

Seems like the flag is not correct. Lets continue on with the rest of the code.
 
```java
int val3 = val2 * 31;
if (val3 % 11 == 0 && val3 % 53 == 0) {
     view.setText(R.string.cr);
     return;
}
```

So basically, we have an integer, `x`.
`x/2 <= 700` and `(x/2)*31 must be divisible by 11 and 53`.

So I first tried multiplying `11 x 53 = 583`.
It does not satisfy the conditions.
Then I `583 x 2 = 1166`.
1166 satisfies all the above conditions.

So I tried `dart1166` as the flag.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/woteq932rfnb6ndi9ym4.png)

We got the right flag this time. 