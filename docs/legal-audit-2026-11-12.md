# 法令の点検（2026-11-12）

この頁は、2026-11-12 に Claude が行った法令の点検のうち、autonomy-and-self-cultivation の分の記録です。
対象は、README のライセンスの記載、引用の仕方の頁（docs/how-to-cite.md）、三篇の紙面と翻刻にある他人の文の引用、書棚（SHELF.md）、投稿用の原稿です。
10 のリポジトリに掛かる免責事項の点検と、条文の取り寄せ方は、cpsbvbng26-dotcom の[点検の記録](https://github.com/cpsbvbng26-dotcom/cpsbvbng26-dotcom/blob/main/docs/legal-audit-2026-11-12.md)にあります。
この頁は運営者の立場を記録するもので、読む人への法的な助言ではありません。

## やり方

法令が出てくる箇所を一つずつ挙げ、挙げた条の文を、取り寄せた条文と照らしました。
条文は記憶から書いていません。
Sophaxis の取り寄せの仕事を走らせて e-Gov から取り寄せ、cpsbvbng26-dotcom の [verification/statutes.json](https://github.com/cpsbvbng26-dotcom/cpsbvbng26-dotcom/blob/main/verification/statutes.json) に写しました。
この頁が挙げる条がどれもその表にあることは、cpsbvbng26-dotcom の `check_ecosystem.js` が確かめます。
判定は、誤り・根拠不足・漏れ・表現・問題なしの五つです。

## 点検の表

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| README「ライセンス」、LICENSE、LICENSE-CODE、CITATION.cff、.zenodo.json | 著作権法第21条、著作権法第23条 | 複製と公衆送信は著作者の権利で、他人に許す範囲は許す者の表示で決まる | LICENSE が CC BY 4.0、LICENSE-CODE が MIT。CITATION.cff と .zenodo.json は CC BY 4.0 だけを書く。引く対象は論文と文書で、コードの MIT は README の表と LICENSE-CODE にある | 問題なし | なし |
| README の「出典を示せば」、docs/how-to-cite.md の同じ句 | 著作権法第21条、CC BY 4.0 の第 3 節 | 第 3 節は、著作者の表示・著作権の表示・ライセンスへの言及・保証の否認への言及・URI・改変したかどうかの表示を求める | 「出典を示せば」は第 3 節の一部しか言っていなかった | 表現 | 「CC BY 4.0 の第 3 節が求める表示（著作者の名、ライセンスへのリンク、改変したかどうかなど）を添えれば」に直した |
| 三篇の紙面（pdf/）と翻刻（papers/）にある他人の文 | 著作権法第32条、著作権法第48条 | 公表された著作物を、公正な慣行に合致し、報道・批評・研究その他の引用の目的上正当な範囲内で引く。出所を明示する | 三篇の引用符の句を標本として見た。どれも短い句で、著者と年を添えている（Schopenhauer 1844/1966、Nietzsche 1967 など）。全部の句を原典と照らしてはいない（SHELF.md が 38 冊を未確認と書く） | 問題なし | 紙面は凍結してあり、変えない |
| 書棚（SHELF.md） | 著作権法第2条 | 著作物は思想又は感情を創作的に表現したもの | 書誌の事実と、論文がどう使ったかだけを書き、本の中身の要約を置かない | 問題なし | なし |
| 紙面が名を挙げる思想家 | 刑法第230条、刑法第230条の2 | 公然と事実を摘示して人の名誉を毀損すること | 名は、著作についての批評と研究の文に出る。人についての事実の摘示は無い | 問題なし | なし |
| 投稿用の原稿（submission/） | 著作権法第21条 | 複製と公衆送信は著作者の権利で、他人に許す範囲は許す者の表示で決まる | Conatus に出す原稿を、CC BY 4.0 の公開版と同じ本文で置く。誌の著作権と許諾の方針は取り寄せていない | 根拠不足 | 記録だけ。CC BY 4.0 の第 2 節は許諾を取り消せないもの（irrevocable）と書くので、公開版の許諾は誌の方針では変わらない |

## 2026-11-12 の続き：リスクを締めた

同じ日に、利用者が「法的リスクをさらにシメて」と求めました。
上の表で根拠不足としたところと、取り寄せた文だけでは読みが決まらないところを、厳しいほうの読みで見直しました。
厳しいほうの読みでも成り立つ形があり、費用が掛からないときは、その形を採りました。
決めたことは、行ごとに理由と一緒に書きます。
取り寄せられなかった文に頼るところは、この節では扱っていません。

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| README の「外部の反応」（cpsbvbng26-dotcom の docs/external-evaluations.md の写し） | 刑法第230条、民法第709条 | 公然と事実を摘示して名誉を毀損すること | 写しは受けた評価と出した先の行で、勧誘の表と出版社の水準の節は写していない。写し元は今日、名指しの出版社についての第三者の評価を外した | 問題なし | なし |
| 三篇の紙面（凍結）が名を挙げる存命の研究者 | 刑法第230条 | 同上 | 名は、著作についての批評と研究の文に出る。紙面は凍結してあり、変えない | 問題なし | なし |
| README の責任の一文 | 民法第709条 | 故意又は過失で他人の権利又は法律上保護される利益を侵害した者は、生じた損害を賠償する | 「責任の範囲は、免責事項に定めています」と書いていた。免責事項は契約ではなく、責任の範囲は法令が決める。今日、免責事項は責任を免除する文をやめた | 表現 | 「責任は、法令の定めるとおりです。説明は免責事項にあります。」に直した。10 のリポジトリで同じ一文にそろえ、cpsbvbng26-dotcom の `check_ecosystem.js` が一字一句を見る。2026-11-12 に Claude が決めました。免責事項が範囲を決めると読める言い方は、どちらの読みでも成り立たないからです |

## 2026-11-12 の続き：取り寄せた周辺の文

上の表で取り寄せられなかった文のうち、同じ日に Sophaxis の取り寄せの仕事が取り寄せたものがあります。
置き場は Sophaxis の main（コミット 6b40d77、PR #218）の `verification/sources-raw.json` です。
取り寄せた文で、上の結論を一つずつ確かめ直しました。
条の文は cpsbvbng26-dotcom の `verification/statutes.json` に写し、`check_ecosystem.js` が Sophaxis の文と一字一句を突き合わせます。
規約は著作物なので、頼った句だけをこの表に引きます。

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| 引用の扱い（判例に代わる行政の解説） | 著作権法第32条、著作権法第48条 | 文化庁の著作権テキスト（令和8年度版）は、引用の条件に、すでに公表された著作物であること、公正な慣行に合致すること（引用の必然性、カギ括弧などで引用部分が明確であること）、正当な範囲内であること（主従関係が明確、分量が必要最小限度、本文が引用文より高い存在価値を持つ）、出所の明示を挙げる。判例ではなく行政の解説 | このリポジトリが他人の文を引くところは、上の表の行のとおり、短い句を括弧に入れ、出所を添え、自分の文の従として置いている | 問題なし | 結論は変えない。判例そのものは取り寄せられなかった（下の一覧） |
| 投稿用の原稿（submission/）と Conatus | Conatus の著作権と投稿の頁（Wayback の写し、2026-07-16 と 2026-08-11） | 誌は、最初に掲載する非独占のライセンスを受け、掲載した版を CC BY-NC 4.0 で公開する。著者は著作権を持ち続ける。投稿前と投稿中にオンラインで公開することを、許し、勧めている（`Authors are permitted and encouraged to post their work online`）。投稿者は、これまで出版されていないことを宣言する | 公開版は CC BY 4.0 で、著作権は著者にある。投稿は机上で返されている | 問題なし | 結論を確かめた。誌の版に付く CC BY-NC 4.0 は誌の版だけに掛かり、CC BY 4.0 の第 2 節が取り消せないとする公開版の許諾は変わらない |

## 2026-11-12 の続き：二度目の見落とし

同じ日に、読むだけの点検を、さらに別の手でもう一度行いました。
上の節が見落としていたものが見つかりました。
前の行は、そのとき何を確かめたかの記録なので、消していません。
法令の文は、cpsbvbng26-dotcom の `verification/statutes.json` に写した取り寄せた文から引きます。
10 のリポジトリに同じものを置く文書の点検は、[cpsbvbng26-dotcom の記録](https://github.com/cpsbvbng26-dotcom/cpsbvbng26-dotcom/blob/main/docs/legal-audit-2026-11-12.md)の同じ見出しの節にもあります。

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| SECURITY.md | 民法第709条 | 取り寄せた文は「故意又は過失によって他人の権利又は法律上保護される利益を侵害した者は、これによって生じた損害を賠償する責任を負う」と定める。無い窓口を約して、頼った人に損を生じさせないこと | SECURITY.md は、安全の問題を GitHub の非公開の報告で受けると約していた。GitHub の API は、2026-11-12 に、このリポジトリの非公開の報告を `enabled: false` と返した。これはリポジトリの設定であり、Claude の持つ道具では変えられない | 誤り | 運営者の ORCID の記録にあるメールアドレスで受けると書き直し、GitHub の非公開の報告は有効になっていないと、確かめた日と一緒に書いた。写しは 10 のリポジトリと deposit-check で一字一句同じで、cpsbvbng26-dotcom の `check_ecosystem.js` の 12j が中身を確かめる。2026-11-12 に Claude が決めました。在る窓口は、免責事項がすでに使っている一つだけだからです |

## 2026-11-12 の続き：四度目の見落とし

同じ日に、読むだけの点検を、四度目に別の手で行いました。
上の節が見落としていたものが見つかりました。
前の行は、そのとき何を確かめたかの記録なので、消していません。
誤っていた前の行は、新しい行の中でそう書き、理由を添えます。
法令の文は、cpsbvbng26-dotcom の `verification/statutes.json` に写した取り寄せた文から引きます。
10 のリポジトリと deposit-check に同じ形で置く文の点検は、[cpsbvbng26-dotcom の記録](https://github.com/cpsbvbng26-dotcom/cpsbvbng26-dotcom/blob/main/docs/legal-audit-2026-11-12.md)の同じ見出しの節にもあります。

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| README「ライセンス」 | 著作権法第21条 | 取り寄せた文は「著作者は、その著作物を複製する権利を専有する。」と定める（cpsbvbng26-dotcom の `verification/statutes.json`、SHA-256 `a85d04f2fd20d7867d5579bee40676b13405c58ea7fd7eb27f1e7a5a03bda100`）。許せるのは、許す者が権利を持つものだけである。ライセンスの文が、他人の文まで許すと読めないこと | README のライセンスの節は、文書の CC BY 4.0 とコードの MIT だけを書き、引いた他人の文の扱いを書いていなかった。Sophaxis は、最初の見落としの節で同じ一文を足していたが、10 のリポジトリと deposit-check には届いていなかった。上の点検の表の「README「ライセンス」、LICENSE、LICENSE-CODE、CITATION.cff、.zenodo.json」の行は問題なしとしていたが、他人の文の扱いを見ていなかった | 漏れ | README のライセンスの節に「このリポジトリが引き、または引用を確かめるために置いている他人の文は、CC BY 4.0 でも MIT でも許諾しておらず、それぞれの権利者のものです。」を足した。`check_ecosystem.js` の 12l が、10 のリポジトリと deposit-check の README（英語の README を含む）にこの一文があることを見る。2026-11-12 に Claude が決めました。Sophaxis の README と同じ範囲を、同じ形で書くためです |
| CITATION.cff の message と .zenodo.json の notes | 著作権法第21条 | 同上。引用情報の license の欄は、どの部分に掛かるかを書けないので、その範囲を別の欄で書くこと | CITATION.cff と .zenodo.json の license の欄は CC BY 4.0 で、notes はコードが MIT とだけ書いていた。欄が文書と論文だけに掛かることは、どこにも書いていなかった。上の点検の表の「README「ライセンス」、LICENSE、LICENSE-CODE、CITATION.cff、.zenodo.json」の行は問題なしとしていたが、欄の掛かる範囲と他人の文を見ていなかった | 表現 | message と notes に、文書と論文が CC BY 4.0、verification/ と build.js のコードが MIT で、license の欄は文書と論文だけに掛かることを書いた。他人の文は許諾していないとも、和英で書いた。`check_ecosystem.js` の 12l が、二つのファイルにこの文があり、置き方が目録の licenceLayout と同じことを見る。2026-11-12 に Claude が決めました。Sophaxis の CITATION.cff が三度目の見落としの節で書いた範囲の文に、10 のリポジトリと deposit-check を揃えるためです |

## 2026-11-12 の続き：八度目の見落とし

読むだけの点検を、八度目に別の手で行いました。
上の節が見落としていたものが見つかりました。
直した日は、日本時間で 2026-11-13 です。
前の行は、そのとき何を確かめたかの記録なので、消していません。
GitHub の利用規約の I 節は「Some Service features may be subject to additional terms specific to that feature or product as set forth in the GitHub Additional Product Terms.」と書きます。
その追加の規約（GitHub Terms for Additional Products and Features）を、これまでの点検は取り寄せていませんでした。
追加の規約は、`github/site-policy` のコミット `166eb97e485b7de3cd5dbaf8c8d16e4310fda46c` の文を、2026-11-13 に raw.githubusercontent.com から直に取り寄せました。
ファイルの SHA-256 は `c39b5a7fc1953ebd37428db18101726acefb55420f766bcd7d912e1b71ee2ffc` です。
Actions の節は「Additionally, regardless of whether an Action is using self-hosted runners, Actions should not be used for:」と書き、次の二つを挙げます。
一つは「Any activity that places a burden on our servers, where that burden is disproportionate to the benefits provided to users (for example, don't use Actions as a content delivery network or as part of a serverless application, but a low benefit Action could be ok if it’s also low burden); or」です。
もう一つは「If using GitHub-hosted runners, any other activity unrelated to the production, testing, deployment, or publication of the software project associated with the repository where GitHub Actions are used.」です。
同じ節は「Misuse of GitHub Actions may result in termination of jobs, restrictions in your ability to use GitHub Actions, disabling of repositories created to run Actions in a way that violates these Terms, or in some cases, suspension or termination of your GitHub account.」とも書きます。
このリポジトリのワークフローは、どれも GitHub の実行環境（`ubuntu-latest` か `ubuntu-24.04`）で動きます。
そこで、ワークフローを一つずつ、四つの目的（制作・検査・配備・公開）のどれに当たるか、負荷が益に見合うかで読みました。
ワークフローの行は、箇所の欄を `.github/workflows/` のファイルの名で始めます。
実行の時間は、GitHub の API で 2026-11-13 に読んだ直近の実行（多くて 300 件）の中央値です。
GitHub Pages が枝から頁を配るときに GitHub が動かす仕事と、Dependabot の版の更新は、このリポジトリのファイルではないので、表に挙げていません。
引いた文は、cpsbvbng26-dotcom の `verification/statutes.json` の「GitHub の利用規約 I」と「GitHub の追加製品の規約 Actions」に写しました。
同じ点検は、13 のリポジトリの記録の同じ見出しの節にあります。

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| GitHub の追加製品の規約（Actions の節） | GitHub の利用規約 I、GitHub の追加製品の規約 Actions | 使っているサービスの規約を取り寄せて読むこと | 利用規約の I 節は追加の規約を取り込みますが、これまでの点検は追加の規約を読んでいませんでした | 漏れ | 取り寄せ、Actions の節の文を cpsbvbng26-dotcom の `verification/statutes.json` に写しました。Sophaxis の週ごとの見張りにも足しました。2026-11-13 に Claude が決めました。ワークフローの使い方を決める文なので、ほかの規約と同じに読むためです |
| `.github/workflows/hygiene.yml`（main への push・PR、毎週水曜の 13:18、手で起こすとき） | GitHub の追加製品の規約 Actions | GitHub の実行環境で、リポジトリのソフトウェアのプロジェクトの制作・検査・配備・公開のどれかに当たること。負荷が利用者への益に見合うこと | 依存・権限・固定・秘密の走査（`verification/check_hygiene.py`）を回します。週に一度の実行は、変更の無い日にも混入を見るためです。実行の中央値は 9 秒です | 問題なし | 変えていません。検査に当たり、負荷は週に一度の数秒です |
| `.github/workflows/pages.yml`（main への push、手で起こすとき） | GitHub の追加製品の規約 Actions | GitHub の実行環境で、リポジトリのソフトウェアのプロジェクトの制作・検査・配備・公開のどれかに当たること。負荷が利用者への益に見合うこと | `build.js` で `site/`を組み、GitHub Pages に配ります。実行の中央値は 29 秒です | 問題なし | 変えていません。配備と公開に当たります |
| `.github/workflows/verify.yml`（main への push・PR、手で起こすとき） | GitHub の追加製品の規約 Actions | GitHub の実行環境で、リポジトリのソフトウェアのプロジェクトの制作・検査・配備・公開のどれかに当たること。負荷が利用者への益に見合うこと | このリポジトリの検査を回します（PDF と翻刻の照合、正誤表の監査、散文、サイト）。実行の中央値は 15 秒です | 問題なし | 変えていません。検査に当たります |
| 検査（`verification/check_hygiene.py`） | なし | ワークフローごとの判断を、機械で固めること | ありませんでした | 漏れ | `verification/check_hygiene.py` に 7 番を足し、`.github/workflows/` のどのファイルもこの節の表に行を持ち、無いファイルの行が無いことを確かめます。cpsbvbng26-dotcom の `check_ecosystem.js` の 12o も、13 のリポジトリについて同じことを確かめます。2026-11-13 に Claude が決めました。新しいワークフローを、規約に照らさずに足せないようにするためです |

この表の判定は、漏れ 2、問題なし 3 です。

弁護士は、この節を見ていません。

## 2026-11-12 の続き：十一度目の見落とし

読むだけの点検を、十一度目に別の手で行いました。
上の節が見落としていたものが見つかりました。
直した日は、日本時間で 2026-11-13 です。
前の行は、そのとき何を確かめたかの記録なので、消していません。
見つかったものは二つです。
一つ目は、PhilArchive の `NEMFSI`（断章論）です。CITATION.cff、README の公開先の表、断章論の翻刻の冒頭の書誌表は、`NEMFSI` を、削除の依頼を書かずに挙げていました。
二つ目は、三篇がそろって SSRN にあると読める文です。README の冒頭、正誤表の冒頭、引用の書き方の頁が、そう書いていました。断章論は SSRN に弾かれており、SSRN にはありません。
削除の依頼と SSRN に弾かれたことは、cpsbvbng26-dotcom の `docs/doi-index.md` と `docs/submission-disclosure.md` に記録があります。
PhilArchive の頁は作業環境から開いておらず、いまの状態は確かめていません。
同じ見落としの記録は、cpsbvbng26-dotcom の同じ見出しの節にもあります。
翻刻の冒頭の書誌表は、`verification/check_fidelity.py` が照合する範囲の外です。照合は Abstract から始まり、書誌表と日本語の要旨はこのリポジトリのために書き下ろしたものだと、その説明に書いてあります。
そのため、書誌表の行は直し、翻刻の本文には触れていません。

| 箇所 | 法令と条 | 要件 | 事実 | 判定 | 対応 |
| --- | --- | --- | --- | --- | --- |
| CITATION.cff の断章論の識別子（`identifiers`）の説明 | なし（引用情報が書く事実） | 記録にある事実だけを書くこと | `NEMFSI` の URL を「PhilArchive の掲載ページ」とだけ書いていました | 表現 | 説明に、2026-09-26 に削除を依頼したことと、いまの状態をここから確かめていないことを足しました。2026-11-13 に Claude が決めました。引用情報を読む人に、所在の頁と同じ事実を見せるためです |
| README の「公開先」の表の、断章論の行 | なし（README が書く事実） | 記録にある事実だけを書くこと | SSRN の欄は「—」だけで、PhilArchive の欄は `NEMFSI` のリンクだけでした | 表現 | SSRN の欄に SSRN に弾かれたことを、PhilArchive の欄に削除の依頼の日といまの状態を確かめていないことを書きました。2026-11-13 に Claude が決めました。cpsbvbng26-dotcom の記録と同じ事実を書くためです |
| `papers/fragmentarian-spiritual-individualism.md` の冒頭の書誌表の PhilArchive の行 | なし（書誌表が書く事実） | 記録にある事実だけを書くこと。翻刻の本文を直さないこと | `NEMFSI` のリンクだけでした。書誌表は照合の範囲の外で、このリポジトリのために書いたものです | 表現 | 書誌表の行に、削除の依頼の日といまの状態を確かめていないことを書きました。翻刻の本文は直していません。2026-11-13 に Claude が決めました。書誌表は紙面の写しではないので、直しても照合と食い違わないためです |
| README の冒頭の、著者による公開の一文 | なし（README が書く事実） | 三篇の所在を、所在ごとに正しく書くこと | 三篇について、著者による公開は SSRN・PhilArchive などの窓口で行っていると書いていました。SSRN にあるのは二篇です | 誤り | 著者による公開は Zenodo で行い、SSRN にあるのは二篇だと書き、所在は公開先の表にあると書きました。2026-11-13 に Claude が決めました。冒頭の一文が、表と食い違わないためです |
| ERRATA.md の冒頭の一文 | なし（正誤表が書く事実） | 同じ | 三篇の PDF は Zenodo・SSRN・PhilArchive で公開済みだと書いていました | 誤り | 三篇の PDF は Zenodo で公開済みだと書き、SSRN にあるのは二篇で断章論は SSRN に弾かれたこと、PhilArchive には三篇とも載り断章論の削除を 2026-09-26 に依頼したことを書きました。最終更新の日を 2026年11月13日にしました。2026-11-13 に Claude が決めました。正誤表の冒頭が、紙面の所在を正しく書くためです |
| `docs/how-to-cite.md` の冒頭の一文 | なし（引用の書き方の頁が書く事実） | 同じ | 著者による公開は Zenodo・SSRN・PhilArchive で行っていると、三篇についてまとめて書いていました | 誤り | 著者による公開は Zenodo で行い、独身論と人格的帝国主義は SSRN と PhilArchive にもあること、断章論は SSRN に弾かれたこと、PhilArchive の断章論の削除を依頼したことを書きました。2026-11-13 に Claude が決めました。引く人が、ない所在を探さないためです |
| `papers/celibate-individual.md` と `papers/fragmentarian-spiritual-individualism.md` の冒頭の著者の行 | なし（CLAUDE.md の決めごと 6） | 使わないと決めた語を、自分の散文で名乗らないこと | 著者の行は、PDF の扉に印字された行の写しです。pypdf 6.19.0 で二つの PDF の一頁目から読んだ文字と、同じ語です | 問題なし | そのままにしました。凍結した紙面の写しで、CLAUDE.md が直さないと決めているためです。cpsbvbng26-dotcom の `check_ecosystem.js` の 12r が、この行の形のほかでこの語を許さないことを見ます |

この表の判定は、誤り 3、表現 3、問題なし 1 です。

弁護士は、この節を見ていません。

## 調べた法令

- GitHub の利用規約（I 節）と GitHub の追加製品の規約（Actions の節。2026-11-13 に `github/site-policy` から直に取り寄せた）
- 著作権法（第2条、第21条、第23条、第32条、第48条）
- 刑法（第230条、第230条の2）
- 民法（第709条）
- CC BY 4.0 の法的条項（第 2 節、第 3 節）
- Conatus – Journal of Philosophy の案内と投稿の頁（Wayback の写し）
- 文化庁「著作権テキスト（令和8年度版）」

## 取り寄せられなかった文

- 引用についての判例は取り寄せていません。裁判所の判例の検索は、結果をスクリプトで描く頁で、取り寄せの仕事からは読めませんでした。代わりに文化庁の著作権テキストを取り寄せました。
- 三篇が引く原典の大半は、手元にありません（SHELF.md）。

## 弁護士について

この点検は Claude が行いました。
弁護士は、この点検を見ていません。
