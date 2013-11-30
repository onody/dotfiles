; -*- Mode: Emacs-Lisp ; Coding: utf-8 -*-
;; ------------------------------------------------------------------------
;; @ load-path

(setq load-path (cons "~/.emacs.d/elisp" load-path))

;; まず、install-elisp のコマンドを使える様にします。
(require 'install-elisp)
;; 次に、Elisp ファイルをインストールする場所を指定します。
(setq install-elisp-repository-directory "~/.emacs.d/elisp/")

(require 'auto-complete)
(global-auto-complete-mode t)

;; バックアップを残さない
(setq make-backup-files nil)

;; モードラインに行番号表示
(line-number-mode t)

;; ------------------------------------------------------------------------

;; menu
(tool-bar-mode 0)


;;; smooth-scroll
(require 'smooth-scroll)
(smooth-scroll-mode t)

;; font
  (let* ((size 14)
         (asciifont "Menlo")
         (jpfont "Hiragino Maru Gothic ProN")
         (h (* size 10))
         (fontspec)
         (jp-fontspec))
    (setq-default line-spacing 5)
    (set-face-attribute 'default nil :family asciifont :height h)
    (setq fontspec (font-spec :family asciifont))
    (setq jp-fontspec (font-spec :family jpfont))
    (set-fontset-font nil 'japanese-jisx0208 jp-fontspec)
    (set-fontset-font nil 'japanese-jisx0212 jp-fontspec)
    (set-fontset-font nil 'japanese-jisx0213-1 jp-fontspec)
    (set-fontset-font nil 'japanese-jisx0213-2 jp-fontspec)
    (set-fontset-font nil '(#x0080 . #x024F) fontspec)
    (set-fontset-font nil '(#x0370 . #x03FF) fontspec))

;; color-theme
(when (require 'color-theme)
     (color-theme-initialize)
     (color-theme-ld-dark))

;; transparency
(setq default-frame-alist
      (append (list
               '(alpha . (90 85))
               ) default-frame-alist))
