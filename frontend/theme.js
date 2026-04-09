(function () {
    var storageKey = "vetpredict-theme";

    function getSavedTheme() {
        var saved = localStorage.getItem(storageKey);
        return saved === "light" || saved === "dark" ? saved : null;
    }

    function preferredTheme() {
        var saved = getSavedTheme();
        if (saved) return saved;
        return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
    }

    function iconFor(theme) {
        return theme === "light" ? "☀" : "☾";
    }

    function labelFor(theme) {
        return theme === "light" ? "Switch to dark mode" : "Switch to light mode";
    }

    function applyTheme(theme) {
        document.documentElement.setAttribute("data-theme", theme);
        localStorage.setItem(storageKey, theme);

        var toggles = document.querySelectorAll("[data-theme-toggle]");
        toggles.forEach(function (btn) {
            btn.textContent = iconFor(theme);
            btn.setAttribute("aria-label", labelFor(theme));
            btn.setAttribute("title", labelFor(theme));
        });
    }

    function toggleTheme() {
        var current = document.documentElement.getAttribute("data-theme") || preferredTheme();
        applyTheme(current === "dark" ? "light" : "dark");
    }

    document.addEventListener("DOMContentLoaded", function () {
        applyTheme(preferredTheme());

        var toggles = document.querySelectorAll("[data-theme-toggle]");
        toggles.forEach(function (btn) {
            btn.addEventListener("click", toggleTheme);
        });
    });
})();
