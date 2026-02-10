<style>
.reveal section[data-background-image] h1:not(:empty) {
  background: rgba(0, 0, 0, 0.6);
  padding: 20px 40px;
  border-radius: 10px;
  display: inline-block;
  color: AliceBlue;
}
</style>

# La facilité trompeuse des code reviews

-v-

## Présentation

Julien Lenormand

<img src="./julien_lenormand_logo.png" alt="" width="786" style="margin-top: 200px" />

---

# Les code reviews, définition

* examiner du code  <!-- .element: class="fragment" -->
* souvent, celui des autres  <!-- .element: class="fragment" -->

Voilà  <!-- .element: class="fragment" -->

-v-

## Usages et bienfaits ?

* comprendre  <!-- .element: class="fragment" -->
* apprendre  <!-- .element: class="fragment" -->
* partager  <!-- .element: class="fragment" -->
* ...  <!-- .element: class="fragment" -->

-v-

## C'est pas si simple !

<img src="./code_review.png" class="r-stretch" alt="" />  <!-- .element: class="fragment" -->

[🔗 lien vers la PR sur GitHub 🐱](https://github.com/Lenormju/talk-code-review/pull/1/changes)  <!-- .element: class="fragment" -->

-v-

## Quelques sujets en vrac

<style>
 .column {
  float: left;
  width: 50%;
}
</style>


<div class="row">
<div class="column">

* variable d'env :
  * convention de nommage
  * checkée tard au runtime
  * `"false"` est `True` (non-empty)
* Commit :
  * Smart
  * message/title
  * semantic
  * signing
* Process :
  * DoD/todolist
  * Test
  * Doc
  * `.env.example`
  * Procédure de déploiement à jour

</div>
<div class="column">

* Monitoring :
  * Log
  * structured
  * observability metric

* Goal :
  * (in)complétude
  * feature flag vs branche/version
  * besoin métier ? (pas tech)
  * dette technique ? ticket pour la résorber

</div>
</div>

---

# Questions (et pensez au ROTI)

---

## Abstract

On vous demande de relire une merge request sur une base de code dont vous n'êtes pas familier. Un "simple" changement de "juste" 3 lignes. Y'a juste à cliquer sur "Approve" !

Essayons de résister à la tentation : faisons collectivement une code review approfondie de cette merge request, de ce qui est visible, mais aussi et surtout de ce qui ne l'est pas.

Cela nous permettra d'échanger sur nos pratiques, d'en découvrir d'autres, et de souligner le rôle crucial de la code review dans le process d'une équipe.
