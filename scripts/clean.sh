rm -rf deb_dist
rm -rf dist
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf
