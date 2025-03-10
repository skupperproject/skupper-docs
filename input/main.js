/*
 *
 * Licensed to the Apache Software Foundation (ASF) under one
 * or more contributor license agreements.  See the NOTICE file
 * distributed with this work for additional information
 * regarding copyright ownership.  The ASF licenses this file
 * to you under the Apache License, Version 2.0 (the
 * "License"); you may not use this file except in compliance
 * with the License.  You may obtain a copy of the License at
 *
 *   http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing,
 * software distributed under the License is distributed on an
 * "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
 * KIND, either express or implied.  See the License for the
 * specific language governing permissions and limitations
 * under the License.
 *
 */

"use strict";

const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

Element.prototype.$ = function () {
  return this.querySelector.apply(this, arguments);
};

Element.prototype.$$ = function () {
  return this.querySelectorAll.apply(this, arguments);
};

window.addEventListener("load", () => {
    let path = window.location.pathname;
    let child = $("#-left-site-nav").firstChild;

    if (path.charAt(path.length - 1) === "/") {
        path += "index.html";
    }

    while (child) {
        if (child.nodeType === 1 && child.id !== "-logotype") {
            let prefix = new URL(child.href).pathname.slice(0, -10);

            if (path.startsWith(prefix)) {
                child.classList.add("selected");
            }
        }

        child = child.nextSibling;
    }
});

window.addEventListener("load", () => {
    let oldTocLinks = $("#-toc > div");

    if (!oldTocLinks) {
        return;
    }

    let headings = $$("h2");

    if (headings.length == 0) {
        return;
    }

    let newTocLinks = document.createElement("div");

    for (let heading of headings) {
        let link = document.createElement("a");
        let text = document.createTextNode(heading.textContent);

        link.setAttribute("href", `#${heading.id}`);
        link.appendChild(text);

        newTocLinks.appendChild(link);
    }

    oldTocLinks.parentNode.replaceChild(newTocLinks, oldTocLinks);

    $("#-toc").style.display = "block";
});

window.addEventListener("load", () => {
    let tocLinks = $("#-toc > div");

    if (!tocLinks) {
        return;
    }

    let updateHeadingSelection = () => {
        let currHash = window.location.hash;

        if (!currHash) {
            return;
        }

        for (let link of tocLinks.$$("a")) {
            let linkHash = new URL(link.href).hash;

            if (linkHash === currHash) {
                link.classList.add("selected");
            } else {
                link.classList.remove("selected");
            }
        }
    }

    window.addEventListener("load", updateHeadingSelection);
    window.addEventListener("hashchange", updateHeadingSelection);
});

window.addEventListener("load", () => {
    let updateScrollState = () => {
        if (window.scrollY > 20) {
            $("body").classList.add("scrolled");
        } else {
            $("body").classList.remove("scrolled");
        }
    };

    updateScrollState();
    window.addEventListener("scroll", updateScrollState);
});

window.addEventListener("load", () => {
    let pathNav = $("#-path-nav");

    if (pathNav.$$("a").length > 1) {
        $("section:first-of-type > div").style.paddingTop = "9.5em";
        $("#-toc").style.top = "9.5em";
        $("html").style.scrollPaddingTop = "9em";

        pathNav.style.display = "inherit";
    }
});

window.addEventListener("load", () => {
    let button = $("#-site-menu-button");
    let layer = $("#-site-menu-layer");

    button.addEventListener("click", () => {
        layer.style.display = "inherit";
    });

    layer.addEventListener("click", (e) => {
        if (e.target === layer) {
            layer.style.display = "none";
        }
    });
});

if (navigator.clipboard) {
    window.addEventListener("load", () => {
        for (let pre of $$("pre")) {
            const code = pre.$("code");

            if (!code) continue;

            if (code.textContent.trim().startsWith("$")) continue;

            const button = document.createElement("a");
            button.classList.add("copy-button");

            const span = document.createElement("span");
            span.textContent = "content_copy";
            span.classList.add("material-icons");

            button.appendChild(span);
            pre.insertBefore(button, pre.firstChild);

            button.addEventListener("click", () => {
                navigator.clipboard.writeText(code.textContent.trim());
            });
        }
    });
}
