<p align="center">
  
  <img src="https://github.com/AminAliH47/PicoStyle/blob/main/static/img/logo-image.png?raw=true" alt="PicoStyle" width="40%">
  
  <p align="center">
    <i>
    Advance market place website written in django :)
    </i>
  </p>
  
  <hr>
</p>

<p>
Online fashion store for wholesalers and retailers. <br>
🗒 Note: This project does not have a shopping cart and wholesalers can register their order through WhatsApp.
</p>

<h3>
⭐️ PicoStyle features 
</h3>

<ul>
  <li>
    Market place
  </li>
  <li>
    Advance admin panel
  </li>
  <li>
    Multilanguage
  </li>
  <li>
    Multilayer filtering
  </li>
  <li>
    Advance category system
  </li>
  <li>
    Session-based favorite list (wish list)
  </li>
  <li>
    Newsletter
  </li>
  <li>
    News system
  </li>
</ul>

<hr>

<h3>
⚙️ Config the project
</h3>

<p>
First you should make venv for this project.
So in the main root of project you should type this command in your Terminal or Console: 
</p>
<pre>
python -m venv venv
</pre>
<p>
Now you should activate your venv.
So in the main root of project you should type this command in your Terminal or Console: 
</p>
<b>
In Linux/macOS:
</b>
<pre>
source venv/bin/activate
</pre>
<b>
In Windows:
</b>
<pre>
venv/Scripts/activate.ps1
</pre>

<p>
After activating venv you should install the <b>requirements.txt</b> packages. So type this command in your Terminal or Console: 
</p>
<pre>
pip install -r requirements.txt
</pre>
<h5>
Configuration of project almost done.
</h5>

<hr>

<h3>
🏁 Run the project
</h3>
<p>
First of all, please enter the following command in the Terminal or Console to make sure the project is configured correctly:
</p>
<pre>
python manage.py check
</pre>
<p>
You should see This message:
  <strong>
    <i>
      "System check identified no issues (0 silenced)."
    </i>
  </strong>
  <br>
  If you see this message you should create your project database. So type this commands in Terminal or Console:
</p>

<pre>
python manage.py makemigrations
</pre>
<pre>
python manage.py migrate
</pre>

<p>
After creating the project database, you should run project. So type this command in Terminal or Console:
</p>
<pre>
python manage.py runserver 4040
</pre>

<h4>
Congratulations, you ran the project correctly ✅
</h4>

<p>
Now copy/paste this address in your browser URL bar:
</p>
<pre>
http://127.0.0.1:4040/
</pre>

<hr>

<h3>
✅ Use the project
</h3>

<p>
For use the project first you should create a superuser. So type this command in Terminal or Console:
</p>
<pre>
python manage.py createsuperuser
</pre>
<p>
After creating a superuser you can login into your admin panels.
</p>

> Advance admin panel login URL:
<pre>
http://127.0.0.1:4040/en/account/login?next=/account/
</pre>
> Main admin panel (django admin panel) login URL:
<pre>
http://127.0.0.1:4040/en/pico-style/login/?next=/en/pico-style/
</pre>

<hr>
<h4>
⭐️ Now you can use all the features of PicoStyle.
</h4>

<p>
To make full and practical use of PicoStyle, we are preparing a simple tutorial that you can see in the same repository wiki.
<b>
  <a href="https://github.com/AminAliH47/PicoStyle/wiki">PicoStyle Wiki</a>  
</b>
</p>

<br>
<h6 align="center">
  Licensed by <b>Coilaco</b>
</h6>
