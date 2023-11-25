window.dash_clientside = window.dash_clientside || {};
window.dash_clientside.my_clientside_library = {
    close_window: function (response) {
        console.log("window will be closed in 5 seconds");
        setTimeout(function () {
            window.close();
        }, 5000);
        return "worked";
    }
}