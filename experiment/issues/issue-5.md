<!-- title: Math breaks my page layout -->
Since switching our blog to mistune with the `math` plugin, some posts look broken: the paragraph is split in two and the rest of the text jumps below the equation, and our HTML validator complains about the page.

It seems to happen in posts where authors write equations in the middle of a sentence, like

    The famous relation $$E=mc^2$$ changed physics.

Posts with equations on their own lines look fine. Not sure if this is a bug or if we are using it wrong, but could this be made to work nicely? We use MathJax on the frontend.
