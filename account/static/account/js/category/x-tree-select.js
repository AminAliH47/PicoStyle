var fullArr = [];
!(function (o) {
    "use strict";
    o.fn.treeSelect = function (t) {
        (o.treeselect_animation = { none: "", "x-flip": "anim xout", fade: "xfade", slide: "xslide" }), void 0 === o.xtsStore && ((o.scbCounter = -1), (o.xtsStore = []), (o.currentCounter = 0)), (o.xts = this);
        var s = o.extend(
            {
                datatree: [],
                transition: "fade",
                direction: "ltr",
                onOpen: function () {},
                onSelect: function (t) {},
                onChange: function (t, e) {},
                onClose: function () {},
                selectablePrernt: !1,
                mainTitle: "Main category",
                json: { title: "title", value: "value", child: "child" },
                searchable: !1,
            },
            t
        );
        return (
            (o.navigatex = []),
            (o.lastx = { title: "", id: "" }),
            (this.target = null),
            (this.text = null),
            o.scbCounter++,
            (o.xtsStore[o.scbCounter] = s),
            (this.init = function (r) {
                (o.lastx.title = s.mainTitle), o(r).hide();
                var t = "Please select";
                void 0 !== o(r).attr("placeholder") && (t = o(r).attr("placeholder"));
                var e = "";
                "rtl" === o.xtsStore[o.scbCounter].direction && (e = "xts-rtl"),
                    o(r)
                        .parent()
                        .append('<div class="xtsel ' + e + '" data-trcounter="' + o.scbCounter + '" >' + t + "</div>"),
                    (s.datatree = o.xts.makeId("1", s.datatree)),
                    o(r)
                        .parent()
                        .find(".xtsel")
                        .bind("click.open", function (t) {
                            if (t.target === this) {
                                var e,
                                    s = o(this);
                                if (!s.hasClass("loading"))
                                    if (
                                        (s.addClass("loading"),
                                        setTimeout(function () {
                                            s.removeClass("loading");
                                        }, 600),
                                        (o.currentCounter = o(this).data("trcounter")),
                                        (o.lastx.title = o.xtsStore[o.currentCounter].mainTitle),
                                        o(this).hasClass("active"))
                                    ) {
                                        if (t.target !== this) return;
                                        o(this).removeClass("active"),
                                            o("#xtsel-list").slideUp(100, function () {
                                                o(this).remove();
                                            });
                                    } else {
                                        o.xtsStore[o.currentCounter].onOpen(),
                                            o.xtsStore[o.currentCounter].searchable
                                                ? ((e = ' class="xts-searcable" '),
                                                  o(document).on("keyup", "#xtsel-list .srch", function () {
                                                      var t = o(this).closest(".xtsel").data("trcounter"),
                                                          e = o(this).val();
                                                      if (0 == e.length) return o.xts.showTree(o.xtsStore[t].datatree), o("#xtsel-list .srch").focus(), !1;
                                                      var s = o.xts.searchShow(t, e, o.xtsStore[t].datatree);
                                                      o("#xtsel-list .xli").remove(), o("#xtsel-list").append(s);
                                                  }))
                                                : (e = ""),
                                            (o.xts.target = o(this).parent().find("input")),
                                            (o.xts.text = o(r).parent().find(".xtsel")),
                                            o(this).append("<ul" + e + ' id="xtsel-list"></ul>'),
                                            void 0 === o.xtsStore[o.currentCounter].navx
                                                ? o.xts.showTree(o.xtsStore[o.currentCounter].datatree)
                                                : ((o.lastx = o.xtsStore[o.currentCounter].lastx),
                                                  (o.navigatex = o.xtsStore[o.currentCounter].navx),
                                                  o.xts.showTree(o.xts.findTree(o.xtsStore[o.currentCounter].datatree, o.xtsStore[o.currentCounter].lastx.id))),
                                            o("#xtsel-list").slideDown(function () {
                                                o(document).bind("click.handvarrsl", function (t) {
                                                    return (
                                                        o(t.target).is(".xtsel-childer, .xtsel-back, .search, .srch") ||
                                                            (o.xts.resetClose(),
                                                            o("#xtsel-list").slideUp(200, function () {
                                                                o(this).remove();
                                                            }),
                                                            o(o.xts.text).removeClass("active")),
                                                        t.preventDefault(),
                                                        !1
                                                    );
                                                });
                                            }),
                                            o(this).addClass("active");
                                    }
                            }
                        }),
                    o(document).off("click", "#xtsel-list li"),
                    o(document).on("click", "#xtsel-list li", function (t) {
                        var e, s, r;

                        let txt = o(this).text().toLowerCase();
                        if (txt.includes("bag")) {
                            document.querySelectorAll(".bag-field").forEach((item) => {
                                item.style.display = "block";
                            });
                            document.querySelectorAll(".shoe-field").forEach((item) => {
                                item.style.display = "none";
                            });
                        } else if (txt.includes("shoe")) {
                            document.querySelectorAll(".shoe-field").forEach((item) => {
                                item.style.display = "block";
                            });
                            document.querySelectorAll(".bag-field").forEach((item) => {
                                item.style.display = "none";
                            });
                        } else if (txt.includes("clothing")) {
                            document.querySelectorAll(".shoe-field").forEach((item) => {
                                item.style.display = "none";
                            });
                            document.querySelectorAll(".bag-field").forEach((item) => {
                                item.style.display = "none";
                            });
                            document.querySelector("#size-field").style.display = "block";
                            document.querySelector("#size-info-field").style.display = "block";
                        } else if (txt.includes("accessories")) {
                            document.querySelectorAll(".shoe-field").forEach((item) => {
                                item.style.display = "none";
                            });
                            document.querySelectorAll(".bag-field").forEach((item) => {
                                item.style.display = "none";
                            });
                            document.querySelector("#size-field").style.display = "block";
                            document.querySelector("#size-info-field").style.display = "block";
                        }

                        o(this).hasClass("xtsel-childer") && !o(t.target).hasClass("xtsel-selectable")
                            ? ((e = { title: o.lastx.title, id: o.lastx.id }),
                              o.navigatex.push(e),
                              (o.lastx.title = o(this).text()),
                              (o.lastx.id = o(this).data("id")),
                              o("#xtsel-list").addClass(o.treeselect_animation[o.xtsStore[o.currentCounter].transition]),
                              (s = this),
                              setTimeout(function () {
                                  o.xts.showTree(o.xts.findTree(o.xtsStore[o.currentCounter].datatree, o(s).data("id"))), o("#xtsel-list").removeClass(o.treeselect_animation[o.xtsStore[o.currentCounter].transition]);
                              }, 600))
                            : o(this).hasClass("xtsel-back")
                            ? (void 0 !== o.navigatex[o.navigatex.length - 1]
                                  ? ((o.lastx.title = o.navigatex[o.navigatex.length - 1].title), (o.lastx.id = o.navigatex[o.navigatex.length - 1].id))
                                  : ((o.lastx.title = o.xtsStore[o.currentCounter].mainTitle), (o.lastx.id = "")),
                              o.navigatex.pop(),
                              (r = o.xts.findTree(o.xtsStore[o.currentCounter].datatree, o(this).data("id"))),
                              o("#xtsel-list").addClass(o.treeselect_animation[o.xtsStore[o.currentCounter].transition]),
                              setTimeout(function () {
                                  0 === r.length ? o.xts.showTree(o.xtsStore[o.currentCounter].datatree) : o.xts.showTree(r), o("#xtsel-list").removeClass(o.treeselect_animation[o.xtsStore[o.currentCounter].transition]);
                              }, 600))
                            : o(t.target).hasClass("search") ||
                              o(t.target).hasClass("srch") ||
                              (o.xtsStore[o.currentCounter].onChange({ value: o(o.xts.target).val(), text: o(o.xts.text).clone().children().remove().end().text() }, { value: o(this).data("value"), text: o(this).text() }),
                              o(o.xts.target).val(o(this).data("value")),
                              o(o.xts.text).text(o(this).text()),
                              0 < o.navigatex.length
                                  ? ((o.xtsStore[o.currentCounter].navx = o.navigatex), (o.xtsStore[o.currentCounter].lastx = o.lastx))
                                  : (delete o.xtsStore[o.currentCounter].navx, delete o.xtsStore[o.currentCounter].lastx),
                              o(o.xts.text).removeClass("active"),
                              o.xtsStore[o.currentCounter].onSelect({ value: o(this).data("value"), text: o(this).text(), id: o(this).data("id"), parent: o.lastx, ancestors: o.navigatex}),
                              o("#xtsel-list").slideUp(100, function () {
                                  o(this).remove();
                              }));
                    }),
                    null != o(r).attr("value") && "" != o(r).val() && null != o(r).val() && this.setDefault(o.scbCounter, o(r).val());
            }),
            (this.makeId = function (t, e) {
                var s = [];
                for (var r in e) {
                    var n = e[r],
                        i = t + "-" + (parseInt(r) + 1);
                    (n.idx = i),
                        void 0 === n[o.xtsStore[o.scbCounter].json.child] && (n[o.xtsStore[o.scbCounter].json.child] = []),
                        0 !== n[o.xtsStore[o.scbCounter].json.child].length && (n[o.xtsStore[o.scbCounter].json.child] = o.xts.makeId(i, n[o.xtsStore[o.scbCounter].json.child])),
                        s.push(n);
                }
                return s;
            }),
            (this.showTree = function (t, e) {
                var s,
                    r = "";
                for (var n in (o("#xtsel-list li").remove(),
                0 !== o.navigatex.length
                    ? (r += '<li class="xtsel-back" data-id="' + (s = o.navigatex[o.navigatex.length - 1]).id + '"> &nbsp;' + s.title + "</li>")
                    : (r += '<li class="search"> <input type="search" class="srch" placeholder="search..." value=""> </li>'),
                t)) {
                    var i = t[n],
                        a = ' class="xli xtsel-childer"',
                        l = "";
                    0 === i[o.xtsStore[o.currentCounter].json.child].length ? (a = ' class="xli"') : o.xtsStore[o.currentCounter].selectablePrernt && (l = '<span class="xtsel-selectable"></span>'),
                        (r += "<li" + a + ' data-id="' + i.idx + '"  data-value="' + i[o.xtsStore[o.currentCounter].json.value] + '">' + l + i[o.xtsStore[o.currentCounter].json.title] + "</li>");
                }
                o("#xtsel-list").html(r), void 0 !== e && e();
            }),
            (this.findTree = function (t, e) {
                var s;
                for (var r in t) {
                    if ((s = t[r]).idx === e) return s[o.xtsStore[o.currentCounter].json.child];
                }
                for (var r in t) {
                    if (0 !== (s = t[r])[o.xtsStore[o.currentCounter].json.child].length) {
                        var n = o.xts.findTree(s[o.xtsStore[o.currentCounter].json.child], e);
                        if (0 !== n.length) return n;
                    }
                }
                return [];
            }),
            (this.findItem = function (t, e, s, r) {
                for (var n in (null != (r = r || null)
                    ? o.navigatex.push({ id: r.idx, title: r[o.xtsStore[s].json.title] })
                    : (o.navigatex.push({ id: "", title: o.xtsStore[s].mainTitle }), (o.lastx.title = o.xtsStore[s].mainTitle), (o.lastx.id = "")),
                t)) {
                    var i = t[n];
                    if (i[o.xtsStore[s].json.value] == e) return i;
                    if (null != i[o.xtsStore[s].json.child] && 0 < i[o.xtsStore[s].json.child].length) {
                        o.lastx = { id: i.idx, title: i[o.xtsStore[s].json.title] };
                        var a = this.findItem(i[o.xtsStore[s].json.child], e, s, i);
                        if (0 != a) return a;
                    }
                }
                return o.navigatex.pop(), !1;
            }),
            (this.searchShow = function (t, e, s) {
                var r = "",
                    n = "";
                for (var i in (o.xtsStore[t].selectablePrernt && (n = '<span class="xtsel-selectable"></span>'), s)) {
                    var a = ' class="xli" ',
                        l = s[i];
                    -1 !== l[o.xtsStore[t].json.title].toString().indexOf(e) || -1 !== l[o.xtsStore[t].json.value].toString().indexOf(e)
                        ? null != l[o.xtsStore[t].json.child] && 0 < l[o.xtsStore[t].json.child].length
                            ? ((r += "<li" + (a = ' class="xli xtsel-childer" ') + ' data-id="' + l.idx + '"  data-value="' + l[o.xtsStore[t].json.value] + '">' + n + l[o.xtsStore[t].json.title] + "</li>"),
                              (r += o.xts.searchShow(t, e, l[o.xtsStore[t].json.child])))
                            : (r += "<li" + a + ' data-id="' + l.idx + '"  data-value="' + l[o.xtsStore[t].json.value] + '">' + l[o.xtsStore[t].json.title] + "</li>")
                        : null != l[o.xtsStore[t].json.child] && 0 < l[o.xtsStore[t].json.child].length && (r += o.xts.searchShow(t, e, l[o.xtsStore[t].json.child]));
                }
                return r;
            }),
            (this.setDefault = function (t, e) {
                var s = o.xts.findItem(o.xtsStore[t].datatree, e, t);
                0 != s && ((o.xtsStore[t].lastx = o.lastx), o.navigatex.pop(), (o.xtsStore[t].navx = o.navigatex), o("[data-trcounter='" + t + "']").text(s[o.xtsStore[t].json.title]));
            }),
            (this.resetClose = function () {
                o.xtsStore[o.currentCounter].onClose(), (o.navigatex = []), (o.lastx = { title: o.xtsStore[o.currentCounter].mainTitle, id: "" }), o(document).unbind("click.handvarrsl"), o(document).off("keyup", "#xtsel-list .srch");
            }),
            (this.setValue = function (t) {
                var e = this.html();
                this.html(e + " " + t);
            }),
            this.each(function () {
                o.xts.init(this);
            }),
            this
        );
    };
})(jQuery);
