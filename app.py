from app.views import *


if __name__ == '__main__':
    app.run(debug=True,
         host='0.0.0.0',
         port=9000,
         threaded=True)
