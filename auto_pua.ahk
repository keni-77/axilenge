; auto_pua.ahk
; 実行すると指定のキー列を PUA に置換して入力する（Windows）
; PUA配置は build_font.py と一致させること

#NoEnv
SendMode Input
SetWorkingDir %A_ScriptDir%

; helper: send unicode codepoint
SendUnicode(codepoint) {
    old := ClipboardAll
    Clipboard := ""
    ClipWait, 0.2
    chr := Chr(codepoint)
    Clipboard := chr
    Send ^v
    Sleep 30
    Clipboard := old
}

; === PUA配置 (build_font.py と一致) ===
; E500〜E505: 母音のみ (u, o, a, e, i, q)
; E506〜E518: 子音のみ (t,d,k,g,h,w,s,z,p,b,n,j,l,f,m,x,tx,ng,th)
; E519:       nn
; E51A〜:     音節 (consOrder × vowels, 各子音につき6母音)

; --- 母音のみ ---
::*?:!u::
    SendUnicode(0xE500)
    return
::*?:!o::
    SendUnicode(0xE501)
    return
::*?:!a::
    SendUnicode(0xE502)
    return
::*?:!e::
    SendUnicode(0xE503)
    return
::*?:!i::
    SendUnicode(0xE504)
    return
::*?:!q::
    SendUnicode(0xE505)
    return

; --- nn (子音nの母音なし版) ---
::nn::
    SendUnicode(0xE519)
    return

; --- 音節 (子音+母音) ---
; consOrder: t=0, d=1, k=2, g=3, h=4, w=5, s=6, z=7, p=8, b=9,
;            n=10, j=11, l=12, f=13, m=14, x=15, tx=16, ng=17, th=18
; vowels: u=0, o=1, a=2, e=3, i=4, q=5
; 音節PUA = 0xE51A + consIndex*6 + vowelIndex

; t (consIndex=0, base=0xE51A)
::tu::
    SendUnicode(0xE51A)
    return
::to::
    SendUnicode(0xE51B)
    return
::ta::
    SendUnicode(0xE51C)
    return
::te::
    SendUnicode(0xE51D)
    return
::ti::
    SendUnicode(0xE51E)
    return
::tq::
    SendUnicode(0xE51F)
    return

; d (consIndex=1, base=0xE520)
::du::
    SendUnicode(0xE520)
    return
::do::
    SendUnicode(0xE521)
    return
::da::
    SendUnicode(0xE522)
    return
::de::
    SendUnicode(0xE523)
    return
::di::
    SendUnicode(0xE524)
    return
::dq::
    SendUnicode(0xE525)
    return

; k (consIndex=2, base=0xE526)
::ku::
    SendUnicode(0xE526)
    return
::ko::
    SendUnicode(0xE527)
    return
::ka::
    SendUnicode(0xE528)
    return
::ke::
    SendUnicode(0xE529)
    return
::ki::
    SendUnicode(0xE52A)
    return
::kq::
    SendUnicode(0xE52B)
    return

; g (consIndex=3, base=0xE52C)
::gu::
    SendUnicode(0xE52C)
    return
::go::
    SendUnicode(0xE52D)
    return
::ga::
    SendUnicode(0xE52E)
    return
::ge::
    SendUnicode(0xE52F)
    return
::gi::
    SendUnicode(0xE530)
    return
::gq::
    SendUnicode(0xE531)
    return

; h (consIndex=4, base=0xE532)
::hu::
    SendUnicode(0xE532)
    return
::ho::
    SendUnicode(0xE533)
    return
::ha::
    SendUnicode(0xE534)
    return
::he::
    SendUnicode(0xE535)
    return
::hi::
    SendUnicode(0xE536)
    return
::hq::
    SendUnicode(0xE537)
    return

; w (consIndex=5, base=0xE538)
::wu::
    SendUnicode(0xE538)
    return
::wo::
    SendUnicode(0xE539)
    return
::wa::
    SendUnicode(0xE53A)
    return
::we::
    SendUnicode(0xE53B)
    return
::wi::
    SendUnicode(0xE53C)
    return
::wq::
    SendUnicode(0xE53D)
    return

; s (consIndex=6, base=0xE53E)
::su::
    SendUnicode(0xE53E)
    return
::so::
    SendUnicode(0xE53F)
    return
::sa::
    SendUnicode(0xE540)
    return
::se::
    SendUnicode(0xE541)
    return
::si::
    SendUnicode(0xE542)
    return
::sq::
    SendUnicode(0xE543)
    return

; z (consIndex=7, base=0xE544)
::zu::
    SendUnicode(0xE544)
    return
::zo::
    SendUnicode(0xE545)
    return
::za::
    SendUnicode(0xE546)
    return
::ze::
    SendUnicode(0xE547)
    return
::zi::
    SendUnicode(0xE548)
    return
::zq::
    SendUnicode(0xE549)
    return

; p (consIndex=8, base=0xE54A)
::pu::
    SendUnicode(0xE54A)
    return
::po::
    SendUnicode(0xE54B)
    return
::pa::
    SendUnicode(0xE54C)
    return
::pe::
    SendUnicode(0xE54D)
    return
::pi::
    SendUnicode(0xE54E)
    return
::pq::
    SendUnicode(0xE54F)
    return

; b (consIndex=9, base=0xE550)
::bu::
    SendUnicode(0xE550)
    return
::bo::
    SendUnicode(0xE551)
    return
::ba::
    SendUnicode(0xE552)
    return
::be::
    SendUnicode(0xE553)
    return
::bi::
    SendUnicode(0xE554)
    return
::bq::
    SendUnicode(0xE555)
    return

; n (consIndex=10, base=0xE556)
::nu::
    SendUnicode(0xE556)
    return
::no::
    SendUnicode(0xE557)
    return
::na::
    SendUnicode(0xE558)
    return
::ne::
    SendUnicode(0xE559)
    return
::ni::
    SendUnicode(0xE55A)
    return
::nq::
    SendUnicode(0xE55B)
    return

; j (consIndex=11, base=0xE55C)
::ju::
    SendUnicode(0xE55C)
    return
::jo::
    SendUnicode(0xE55D)
    return
::ja::
    SendUnicode(0xE55E)
    return
::je::
    SendUnicode(0xE55F)
    return
::ji::
    SendUnicode(0xE560)
    return
::jq::
    SendUnicode(0xE561)
    return

; l (consIndex=12, base=0xE562)
::lu::
    SendUnicode(0xE562)
    return
::lo::
    SendUnicode(0xE563)
    return
::la::
    SendUnicode(0xE564)
    return
::le::
    SendUnicode(0xE565)
    return
::li::
    SendUnicode(0xE566)
    return
::lq::
    SendUnicode(0xE567)
    return

; f (consIndex=13, base=0xE568)
::fu::
    SendUnicode(0xE568)
    return
::fo::
    SendUnicode(0xE569)
    return
::fa::
    SendUnicode(0xE56A)
    return
::fe::
    SendUnicode(0xE56B)
    return
::fi::
    SendUnicode(0xE56C)
    return
::fq::
    SendUnicode(0xE56D)
    return

; m (consIndex=14, base=0xE56E)
::mu::
    SendUnicode(0xE56E)
    return
::mo::
    SendUnicode(0xE56F)
    return
::ma::
    SendUnicode(0xE570)
    return
::me::
    SendUnicode(0xE571)
    return
::mi::
    SendUnicode(0xE572)
    return
::mq::
    SendUnicode(0xE573)
    return

; x (consIndex=15, base=0xE574)
::xu::
    SendUnicode(0xE574)
    return
::xo::
    SendUnicode(0xE575)
    return
::xa::
    SendUnicode(0xE576)
    return
::xe::
    SendUnicode(0xE577)
    return
::xi::
    SendUnicode(0xE578)
    return
::xq::
    SendUnicode(0xE579)
    return

; tx (consIndex=16, base=0xE57A)
::txu::
    SendUnicode(0xE57A)
    return
::txo::
    SendUnicode(0xE57B)
    return
::txa::
    SendUnicode(0xE57C)
    return
::txe::
    SendUnicode(0xE57D)
    return
::txi::
    SendUnicode(0xE57E)
    return
::txq::
    SendUnicode(0xE57F)
    return

; ng (consIndex=17, base=0xE580)
::ngu::
    SendUnicode(0xE580)
    return
::ngo::
    SendUnicode(0xE581)
    return
::nga::
    SendUnicode(0xE582)
    return
::nge::
    SendUnicode(0xE583)
    return
::ngi::
    SendUnicode(0xE584)
    return
::ngq::
    SendUnicode(0xE585)
    return

; th (consIndex=18, base=0xE586)
::thu::
    SendUnicode(0xE586)
    return
::tho::
    SendUnicode(0xE587)
    return
::tha::
    SendUnicode(0xE588)
    return
::the::
    SendUnicode(0xE589)
    return
::thi::
    SendUnicode(0xE58A)
    return
::thq::
    SendUnicode(0xE58B)
    return

; 追加マッピングはここに書く
