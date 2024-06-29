<h1 align="center">
  <br>
  <img src="./logo.png" width="35%" height="35%"alt="Walrus Browser Logo.">
  <br>
  <b>Walrus Browser</b>
  <br>
</h1>

<h4 align="center">A simple "browser" coded in Python with the help of PyQt5.</h4>

<p align="center">
  <a href="#download">Download</a> •
  <a href="#compile">Compiling</a> •
  <a href="#running">Running</a> •
  <a href="#usage">Usage</a> •
  <a href="#contributing">Contributing</a>
</p>



<h4 align="center"><i>Supports anything that can run Python and PyQt5.</i></h4>



## Download

The latest compiled versions are available on the [releases page](https://github.com/virgilholmes/walrus/releases/).

## Compile

The only build i have for this is macOS. I only have a macbook and thats what its build for. If you have any other OS and would like to build, get in touch with me on <a href="https://twitter.com/snowtechsupport/">twitter</a>.
here are the steps for building on macOS,

do the first 4 steps in <a href="#running">Running</a> then do this to compile this code.

download the icon.icns file and put it in the root folder of the walrus.py
<a href="https://download.mrsn0ww0lf.repl.co/walrus/mac/icon.icns" download>icon.icns download</a>
```
pip install py2app
```
then download the setup script and put it in the root folder 
<a href="https://download.mrsn0ww0lf.repl.co/walrus/mac/setup.py" download>setup.py download</a>
```
python3 setup.py py2app
```
then in the dist folder, the walrus browser.app should be there.
## Running 
```
git clone https://github.com/virgilholmes/walrus/
```

```
pip install PyQt5
```
```
pip install PyQtWebEngine
```
```
cd walrus
```
```
py walrus.py
```
## Usage

Walrus opens a graphical interface. You have page forward,page back, and a refresh button. You have a home button that leads to a simple html website about this project. The normal new tab site is Google. The Bar at the top does NOT do a search, you must go to the exact webpage.



## Contributing

If you find any bugs or you would like to add a feature, make a [pull request](https://github.com/virgilholmes/walrus/pulls).
