(require 'package)
(add-to-list 'package-archives
    '("elpy" . "http://jorgenschaefer.github.io/packages/"))

(package-initialize)
(elpy-enable)
