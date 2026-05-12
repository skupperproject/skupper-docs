// Licensed to the Apache Software Foundation (ASF) under one
// or more contributor license agreements.  See the NOTICE file
// distributed with this work for additional information
// regarding copyright ownership.  The ASF licenses this file
// to you under the Apache License, Version 2.0 (the
// "License"); you may not use this file except in compliance
// with the License.  You may obtain a copy of the License at
//
//   http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing,
// software distributed under the License is distributed on an
// "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
// KIND, either express or implied.  See the License for the
// specific language governing permissions and limitations
// under the License.

const $ = document.querySelector.bind(document);
const $$ = document.querySelectorAll.bind(document);

Element.prototype.$ = function () {
    return this.querySelector.apply(this, arguments);
};

Element.prototype.$$ = function () {
    return this.querySelectorAll.apply(this, arguments);
};

function createLink(parent, href, text) {
    const elem = document.createElement("a");
    const textNode = document.createTextNode(text);

    elem.setAttribute("href", href);
    elem.appendChild(textNode);

    parent.appendChild(elem);
}

window.addEventListener("load", () => {
    const oldToc = $("#-toc");

    if (oldToc === null) {
        return;
    }

    if (oldToc.children.length !== 0) {
        return;
    }

    const parent = $("h1").parentElement;
    const headings = new Map(); // Element heading => Array of subheadings
    let currHeading = null;
    let currSubheadings = null;

    for (let i = 0; i < parent.children.length; i++) {
        const child = parent.children[i];
        const tag = child.tagName.toLowerCase();

        if (tag === "h2") {
            currHeading = child;
            currSubheadings = [];

            headings.set(currHeading, currSubheadings);
        }

        if (tag === "h3" && currSubheadings) {
            currSubheadings.push(child);
        }
    }

    if (headings.size === 0) {
        // Remove the TOC element so it doesn't affect page layout
        oldToc.remove();

        return;
    }

    const toc = document.createElement("section");
    const tocHeading = document.createElement("h4");
    const tocHeadingText = document.createTextNode("Contents");

    tocHeading.appendChild(tocHeadingText);
    toc.appendChild(tocHeading);
    toc.setAttribute("id", "-toc");

    const tocLinks = document.createElement("nav");

    createLink(tocLinks, "#", "Overview");

    // XXX Another variant I considered
    // createLink(tocLinks, "#", $("h1").textContent);

    for (const [heading, subheadings] of headings) {
        createLink(tocLinks, `#${heading.id}`, heading.textContent);

        if (subheadings.length === 0) {
            continue;
        }

        const sublinks = document.createElement("nav");

        for (const subheading of subheadings) {
            createLink(sublinks, `#${subheading.id}`, subheading.textContent);
        }

        tocLinks.appendChild(sublinks);
    }

    toc.appendChild(tocLinks);
    oldToc.replaceWith(toc);
});

window.addEventListener("load", () => {
    const tocLinks = $("#-toc nav");

    if (!tocLinks) {
        return;
    }

    const updateHeadingSelection = () => {
        const currHash = window.location.hash;

        for (const elem of $$(".selected")) {
            elem.classList.remove("selected");
        }

        if (currHash) {
            for (const link of tocLinks.$$("a")) {
                const linkHash = new URL(link.href).hash;

                if (linkHash === currHash) {
                    link.classList.add("selected");
                    break;
                }
            }

            $(currHash).parentElement.parentElement.classList.add("selected");
        } else {
            // Select the top heading by default
            tocLinks.$("a").classList.add("selected");
        }
    }

    updateHeadingSelection();

    window.addEventListener("hashchange", updateHeadingSelection);
});

window.addEventListener("load", () => {
    for (const block of $$("pre > code.language-console")) {
        const lines = block.innerHTML.split("\n");

        block.innerHTML = lines.map(line => {
            switch (line[0]) {
            case "#":
                return `<span class="shell-comment">${line}</span>`;
            case "$":
                return `<span class="shell-command">${line}</span>`;
            default:
                return `<span class="shell-output">${line}</span>`;
            }
        }).join("\n");
    }
});

window.addEventListener("load", () => {
    for (const elem of $$("div.attribute > div.attribute-heading")) {
        elem.addEventListener("click", () => {
            elem.parentElement.classList.toggle("collapsed");
        });
    }
});

window.addEventListener("load", () => {
    if ($("a#expand-all")) {
        $("a#expand-all").addEventListener("click", () => {
            for (const elem of $$("div.attribute.collapsed")) {
                elem.classList.remove("collapsed");
            }
        });
    }

    if ($("a#collapse-all")) {
        $("a#collapse-all").addEventListener("click", () => {
            for (const elem of $$("div.attribute")) {
                elem.classList.add("collapsed");
            }
        });
    }
});

// // Function to open an image in fullscreen
// function openFullscreen(elem) {
//   if (elem.requestFullscreen) {
//     elem.requestFullscreen();
//   } else if (elem.mozRequestFullScreen) { // Firefox
//     elem.mozRequestFullScreen();
//   } else if (elem.webkitRequestFullscreen) { // Chrome, Safari, and Opera
//     elem.webkitRequestFullscreen();
//   } else if (elem.msRequestFullscreen) { // IE/Edge
//     elem.msRequestFullscreen();
//   }
// }

// // Attach click event listeners to all img elements
// document.querySelectorAll("img").forEach(img => {
//   img.addEventListener("click", () => {
//     openFullscreen(img);
//   });
// });
