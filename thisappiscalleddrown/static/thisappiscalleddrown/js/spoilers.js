function toggleSpoilerAnimated(spoilerElement, isInvertedCollapse, isInvertedExpand, duration = 300) {
    let spoilerBody = spoilerElement.querySelector('.spoiler-body');
    let isCollapsing = spoilerElement.classList.contains('expanded');
    let heightBefore = spoilerElement.offsetHeight;
    let offsetBefore = window.pageYOffset;
    spoilerElement.classList.toggle('expanded', !isCollapsing);
    let isScrollRequired = (isCollapsing && isInvertedCollapse) ||
        (!isCollapsing && isInvertedExpand);
    let scrollFunc = (isScrollRequired)
        ? () => {
            let heightNow = spoilerElement.offsetHeight;
            let heightDelta = heightNow - heightBefore;
            window.scrollTo(0, offsetBefore + heightDelta);
        }
        : undefined;
    slideToggle(spoilerBody, !isCollapsing, {duration: duration, progress: scrollFunc, complete: scrollFunc});
}

for (let el of document.querySelectorAll('.spoiler-btn-top')) {
    el.addEventListener('click', e => toggleSpoilerAnimated(el.parentNode));
}
for (let el of document.querySelectorAll('.spoiler-btn-bottom')) {
    el.addEventListener('click', e => toggleSpoilerAnimated(el.parentNode, true, true));
}

function slideUp(element, options) {
    slideToggle(element, false, options);
}

function slideDown(element, options) {
    slideToggle(element, true, options);
}

function slideToggle(element, isOpening, options) {
    let h0 = getHeight(element);
    let duration = (options && options.duration) || 1000;
    let start = null;

    function step(timestamp) {
        if (!start) {
            start = timestamp;
        }
        let progress = 1.0 * (timestamp - start) / duration;
        let h1 = isOpening ? (h0 * progress) : (h0 * (1 - progress));
        if (progress < 1.0) {
            element.style.height = h1 + 'px';
            if (options.progress) {
                options.progress();
            }
            window.requestAnimationFrame(step);
        } else {
            element.style.height = '';
            element.style.overflow = '';
            if (!isOpening) {
                element.style.display = 'none';
            }
            if (options.complete) {
                options.complete();
            }
        }
    }

    element.style.display = 'block';
    element.style.overflow = 'hidden';
    window.requestAnimationFrame(step);
}

// https://stackoverflow.com/a/29047232/3423843
function getHeight(el) {
    let el_comp_style = window.getComputedStyle(el),
        el_display = el_comp_style.display,
        el_max_height = el_comp_style.maxHeight.replace('px', '').replace('%', ''),
        el_position = el.style.position,
        el_visibility = el.style.visibility,
        wanted_height = 0;

    if (el_display !== 'none' && el_max_height !== '0') {
        return el.offsetHeight;
    }

    el.style.position = 'absolute';
    el.style.visibility = 'hidden';
    el.style.display = 'block';

    wanted_height = el.offsetHeight;

    el.style.display = el_display;
    el.style.position = el_position;
    el.style.visibility = el_visibility;

    return wanted_height;
}