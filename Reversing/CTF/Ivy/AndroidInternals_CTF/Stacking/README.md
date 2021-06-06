# Stacking

My write up is also available at [dev.to/wireless90](https://dev.to/wireless90/stackoverflow-android-internals-ctf-ex7-2l0k)

Get the [executable here](https://github.com/wireless90/AndroidInternalsCTF/tree/main/Stacking)

# Instructions

- Give the program the correct argument so it will print the flag
- It is ok if the program crash afterwards.
- Do not reverse the decrypt function


# Let's Begin

Lets start by running the program in android.

I'll use `adb` to push it to my android device.

```sh
┌──(razali㉿razali)-[~/…/Ivy/AndroidVulnResearch/ctf/stacking]
└─$ adb push a.out /data/local/tmp 
```

Next, run the program in the android device.
```sh
root@hammerhead:/data/local/tmp # ./a.out                                      
usage: ./a.out <username> <password>
root@hammerhead:/data/local/tmp # ./a.out root toor                            
Login failed
```

Seems like we need the right username and password.

Let's open up the program in `IDA` to perform static analysis.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/gkwsiduk0h4uh3rf7th2.png)

In the `functions` window, we can see that there exists a function called `print_flag`. 

Click `x` to find all references of the function within `a.out`![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/r9lsuq2at8jlnsr2ffd5.png)
 . 

We can see that there are actually no references to that function within the program. From the title of this exercise, `stacking`, we know that we need to perform some kind of stack overflow.

Let's take a look at the `main` function in `IDA`.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/0akdmq6863ea9rzfj2zz.png)

There is an interesting function called within the `main` function, `verify_user`. It takes in the username in `R0` and password in `R1` and performs some kind of verification.

 Let's take a deeper look into the function `verify_user`.


![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/3qan3gx0pr7z3clgd6yk.png)

I have marked the first occurrence of username and password. Let's rename the variables by pressing the `n` key and giving them appropriate names.

It will now look like

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/ceajln9haahxm9o43kc0.png)


Looking further below, there are 2 unsafe `strcpy` functions.

The `strcpy` function has the following declaration.
```c
char *strcpy(char *dest, const char *src)
```

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/dx205kfj81jg2cg0f2lp.png)
 
 
Let's focus on the 2nd `strcpy`, marked with asterisk `*`, as the destination variable is closer to the start of the stack.

The destination variable in the above figure is `var_1C`.

Now let's scroll back all the way up to the top of the function to see how far is this variable from the start of the stack.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/373btbe0c11wciam3rox.png)

Yea, its `0x1C` which is 28 bytes from the start of the stack. `IDA` by default names stack variables by how far they are from the start of the stack.

Lets take a look at how a `stack frame` looks like.

![Image](https://azeria-labs.com/wp-content/uploads/2020/03/stack_3_darkbg.png)

As we can see, our goal is to override the `Link Register`. The `Link register` contains the address to return to after completing the current function, `verify`.

So in order to override it , we need to spam 28 bytes + an extra 4 bytes to override the `Frame Pointer`, and our final 4 bytes to override our link register.

Thus lets put an input of 32 'A's followed by 4 'B's.

Lets look at the result in `GDB`.

In our android lets run our `gdbserver`.

```sh
root@hammerhead:/data/local/tmp # ./gdbserver localhost:6666 ./a.out root AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABBBB  
```

In our host, lets connect to it using `gdb-multiarch`.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/472vi3g66749rasbmigr.png)

We can see that our function tried to return to an address `0x42424240` which is our `BBBB`. The reason it is not `0x42424242` is because due to alignment reasons.

Anyway, now we know how to direct the function to point to anywhere we want.

Lets try to point the function to `0xDEADBEEF`.

```sh
root@hammerhead:/data/local/tmp # ./gdbserver localhost:6666 ./a.out root `echo -en "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\xDE\xAD\xBE\xEF" ` 
```
![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/lfqigqg5q3klav8ns13z.png)

Notice that it now points to  `0xEFBEADDC`.


Next, lets get the address of the unreference function `print_flag`.

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/vc35bnyfd4lnti39wwdy.png)
 
The function `print_flag` lies in the address `0x00008530`.

If `0xDEADBEEF` produces `0xEFBEADDC`, we need to input `0x00008530` as `0x30850000`.

```sh
root@hammerhead:/data/local/tmp # ./gdbserver localhost:6666 ./a.out root `echo -en "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA\x30\x85\x00\x00" ` 
```

![image](https://dev-to-uploads.s3.amazonaws.com/uploads/articles/tg7u021vlnp07q0t7bnb.png)


And we got the flag. 