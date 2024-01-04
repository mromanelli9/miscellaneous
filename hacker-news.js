let getCommentURL = (user) => {
	let comments = document.querySelectorAll(".athing.comtr");
	let selected = [...comments].filter(node => node.querySelector("a.hnuser").text == user);
	if (selected.length) {
		return `https://news.ycombinator.com/item?id=${selected[0].id}`;
	} else {
		return undefined;
	}
}