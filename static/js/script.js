/**
 * Author: Tin Tomašić
 */
window.onload = () => {
    enableEmojiCopy();
}

/**
 * Enables copying selected emoji to clipboard
 */
function enableEmojiCopy() {
    document.getElementById('results')?.querySelectorAll('tbody > tr > td:nth-child(2)').forEach(emoji =>
        emoji.onclick = () => navigator.clipboard.writeText(emoji.textContent).then(
            () => {
                const toast = document.getElementById('toast');
                toast.querySelector("#toast-body").innerHTML = `Emoji ${emoji.textContent} successfully copied!`;
                new bootstrap.Toast(toast).show();
            },
            err => console.error('Async: Could not copy text: ', err)
        )
    )
}
