import:py asyncio;

async can say_hello(){
    print("Hello");
    await asyncio.sleep(1);
    print("World!");
}

async can main(){
    await asyncio.gather(
        say_hello(),
        say_hello()
    );
}

with entry {
    asyncio.run(main());
}