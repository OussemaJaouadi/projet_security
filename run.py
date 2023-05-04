from consumer import create_app as front

if __name__ == '__main__':
    front.run(debug=True,port=8000)