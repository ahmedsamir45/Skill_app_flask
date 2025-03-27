let progress = document.querySelectorAll('.skill-progress span')


progress.forEach((span) => {
    span.style.width = span.dataset.width
})
console.log('main2')