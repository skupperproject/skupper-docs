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

// window.addEventListener("load", () => {
//     const oldToc = $("#-toc");

//     if (!oldToc) {
//         return;
//     }

//     const headings = $$("h2");

//     if (headings.length == 0) {
//         oldToc.remove();
//         return;
//     }

//     const newToc = document.createElement("section");
//     const newTocHeading = document.createElement("h4");
//     const newTocHeadingText = document.createTextNode("Contents");

//     newTocHeading.appendChild(newTocHeadingText);
//     newToc.appendChild(newTocHeading);
//     newToc.setAttribute("id", "-toc");

//     const newTocLinks = document.createElement("nav");

//     const topLink = document.createElement("a");
//     const topText = document.createTextNode("Top");

//     topLink.setAttribute("href", "#");
//     topLink.appendChild(topText);

//     newTocLinks.appendChild(topLink);

//     for (const heading of headings) {
//         const link = document.createElement("a");
//         const text = document.createTextNode(heading.textContent);

//         link.setAttribute("href", `#${heading.id}`);
//         link.appendChild(text);

//         newTocLinks.appendChild(link);

//         const subheadings = heading.parentElement.$$("h3");

//         if (subheadings.length == 0) {
//             continue;
//         }

//         const sublinks = document.createElement("nav");

//         for (const subheading of subheadings) {
//             const sublink = document.createElement("a");
//             const subtext = document.createTextNode(subheading.textContent);

//             sublink.setAttribute("href", `#${subheading.id}`);
//             sublink.appendChild(subtext);

//             sublinks.appendChild(sublink);
//         }

//         newTocLinks.appendChild(sublinks);
//     }

//     newToc.appendChild(newTocLinks);
//     oldToc.replaceWith(newToc);
// });

window.addEventListener("load", () => {
    const tocLinks = $("#-toc nav");

    if (!tocLinks) {
        return;
    }

    const updateHeadingSelection = () => {
        const currHash = window.location.hash;

	for (const element of $$(".selected")) {
	    element.classList.remove("selected");
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
            const link = tocLinks.$("a");

            link.classList.add("selected");
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
    for (const element of $$("div.attribute > div.attribute-heading")) {
	element.addEventListener("click", () => {
	    element.parentElement.classList.toggle("collapsed");
	});
    }
});

window.addEventListener("load", () => {
    if ($("a#expand-all")) {
	$("a#expand-all").addEventListener("click", () => {
	    for (const element of $$("div.attribute.collapsed")) {
		element.classList.remove("collapsed");
	    }
	});
    }

    if ($("a#collapse-all")) {
	$("a#collapse-all").addEventListener("click", () => {
	    for (const element of $$("div.attribute")) {
		element.classList.add("collapsed");
	    }
	});
    }
});


// Function to open an image in fullscreen
function openFullscreen(element) {
  if (element.requestFullscreen) {
    element.requestFullscreen();
  } else if (element.mozRequestFullScreen) { // Firefox
    element.mozRequestFullScreen();
  } else if (element.webkitRequestFullscreen) { // Chrome, Safari, and Opera
    element.webkitRequestFullscreen();
  } else if (element.msRequestFullscreen) { // IE/Edge
    element.msRequestFullscreen();
  }
}
// Attach click event listeners to all img elements
document.querySelectorAll('img').forEach(img => {
  img.addEventListener('click', () => {
    openFullscreen(img);
  });
});
