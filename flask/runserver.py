from waitress import serve
import run, os


os.environ['KMP_DUPLICATE_LIB_OK']='True'
serve(run.app, host='127.0.0.1', port=5000)
