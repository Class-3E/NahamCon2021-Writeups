# $Echo - Easy

One of the beginner web challenges, which had a fun CTFy twist to it. 

![image](https://user-images.githubusercontent.com/77645911/111083651-79852900-8506-11eb-9fa9-5231389e23a2.png)

We start off with a web interface with a basic GET form. 

Using `Ctrl + U`, we can see there's nothing extra hidden in the source code (you can never be too cautious with easy web challenges ;) )

Initially enumerating the web server, we can see our input is passed to the server as a GET parameter, then echoed back to us. 

![image](https://user-images.githubusercontent.com/77645911/111084876-84db5300-850c-11eb-8d07-29a9e1e6ec8c.png)


Now, we will try to test the application with special characters, to see if we can get it to break in any way:

![image](https://user-images.githubusercontent.com/77645911/111084813-3463f580-850c-11eb-8460-61ccf9f6cb9f.png)

Huh, that's odd - there seems to be some sort of filter on characters deemed "dangerous" by the application.

Let's try to fuzz these characters, to see which ones we can and can't use. 

There are many tools out there for fuzzing - but we'll create a quick bash script to save a little time, and because who *doesn't* love bash right?

```sh
for character in $(cat special_chars.txt); do
  echo -n "$character : " && curl -s http://challenge.nahamcon.com/?echo=$character | wc -c
done
```

![image](https://user-images.githubusercontent.com/77645911/111084111-ba7e3d00-8508-11eb-8d39-81d40602df56.png)

We can see that the server returns `644` characters when a bad character is detected, so we can simply append `grep -v 644` to the bash script.
This returns a few very interesting characters:

![image](https://user-images.githubusercontent.com/77645911/111085023-5316bc00-850d-11eb-9b52-b2b5db4ae1f9.png)

What particularly catches my eye is the fact backticks are allowed by the server. 
Backticks are very useful, as they can be used to "break-out" of bash commands. 
To demonstrate what I mean by this, when we run the command:

![image](https://user-images.githubusercontent.com/77645911/111085079-a8eb6400-850d-11eb-9312-15758b53c109.png)

It will run the command `whoami` *first*, then insert the output into the `echo` command. 
This can be incredibly useful, as we can gain remote code execution if our output is being passed into the bash command line.

Let's try it!

![image](https://user-images.githubusercontent.com/77645911/111085133-e8b24b80-850d-11eb-9867-deb6bb5c469f.png)

It works - we can see the command `id` has executed on the system. 
Now, let's try to find some more useful information.

We can see using ``ls``, there is the file `index.php` in the current directory. 
This might contain more information about what is actually going on behind the scenes of the interface.


```php
<?php 
$to_echo = $_REQUEST['echo']; 
$cmd = "bash -c 'echo " . $to_echo . "'"; 

if(isset($to_echo)) 
  { if($to_echo=="") 
    { print "Please don't be lame, I can't just say nothing."; }
  
  elseif (preg_match('/[#!@%^&*()$_+=\-\[\]\';,{}|":>?~\\\\]/', $to_echo)) 
    { print "Hey mate, you seem to be using some characters that makes me wanna throw it back in your face >:("; } 
  elseif ($to_echo=="cat") 
    { print "Meowwww... Well you asked for a cat didn't you? That's the best impression you're gonna get :/"; } 
  elseif (strlen($to_echo) > 15) 
    { print "Man that's a mouthful to echo, what even?"; } 
    
  else { system($cmd); } } else { print "Alright, what would you have me say?"; } ?>
```


We can see in the above code, it takes our parameter "echo", and passes it through multiple checks, and if it bypasses them all - it executes it in bash.
The first check uses the `preg_match` function to check if there are any of the "bad" characters in our code. 

The next check simply compares the *whole* command to `cat`, which is easily bypassable by adding some command line flags (like a file), so we can ignore this one.


The most significant line of code we need to view is:
```php
strlen($to_echo) > 15
```
If our input exceeds the length of 15, the program will "crash", and not execute our code. 

Let's just quickly locate the flag file, before we go on:

![image](https://user-images.githubusercontent.com/77645911/111085722-755e0900-8510-11eb-9c9a-9a0c4fcfa58f.png)


This is tricky as the flag file in the parent directory (`../flag.txt`), and the two breakout characters already sum 13 characters.
This means, we need to read the file in two characters - `cat` is four (including the space between the filename)

I did a little digging in bash's man page - as all sane humans should do at 2am in the morning, right...

Luckily, I found something promising, so it justified my late night searching:

![image](https://user-images.githubusercontent.com/77645911/111085567-c4576e80-850f-11eb-93d9-4d3601e67b73.png)

This seems perfect!
We could supposedly read the file, in exactly 15 characters.

And sure enough, when we input our malicious payload, it executes:

![image](https://user-images.githubusercontent.com/77645911/111085595-efda5900-850f-11eb-998f-57b75a8fd5db.png)

## Boom, first flag of the CTF down!

### Afternotes

There are several other special characters that can be used to break out of bash shells. Namely:
```$(id)```

```; id```

````id```` (As shown here)

```&& id```


Keep these in mind for future CTFs ;)
