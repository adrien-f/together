# Together

Together is a Angular/Flask based web application for creating, sharing and editing Youtube playlists.

## Dependencies

Together has been tested with PostgresSQL but should work with MySQL and SQLite. You will need to have coffee script, less and uglify-js installed to compile the assets.

## Installation

Clone the repository, copy `settings_dist.py` to `settings.py` and complete it with your database uri, a secret key and your Youtube API key. And then in a shell:

    pip install -r requirements.txt
    python manage.py assets build
    python manage.py db upgrade
    
You should then be able to run it with:

    python manage.py run.py

## Development

Together is currently in development when I find some time so come back sometime to see what new features I've implemented!

## License

The MIT License (MIT)

Copyright (c) [2014] [@adrien-f]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
