import uvicorn


def main(host="0.0.0.0", port=8009):
    print(666)
    uvicorn.run("pipui.main:app", host=host, port=port)


if __name__ == "__main__":
    main()
