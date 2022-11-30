# paranormal-maimai

This is just a playground for me to mess with SEGA's "maimaiDX International Version" website. If you are a *somewhat-devoted* maimai player, I think you know [where the title comes from](https://www.youtube.com/watch?v=L_M599WSXlc).

# How to play with this

1. Log out from your account: [`https://maimaidx-eng.com/maimai-mobile/home/userOption/logout/?`](https://maimaidx-eng.com/maimai-mobile/home/userOption/logout/?), now you should be at the login page.
2. Open `Inspection Tool` on Chrome (or the equivalent on other browsers) (by using `F12`, or `Ctrl+Shift+I`) and head to `Network` tab.
3. Log in **WITH YOUR SEGA ID** (if you don't have one, just create it)
4. You should see one thing with `/sid`, click on it, scroll down until you see the part "Request Headers", copy the text in `Cookie` section.
5. Head to `accounts.json`, create a pair with the `key` is your SEGA ID account name, `value` is the text
6. Enjoy.

# Known Issues

1. `ERROR CODE: 200004`: idk how to fix :<
