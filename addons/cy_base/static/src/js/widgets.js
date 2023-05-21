odoo.define('cy_base.widgets', function (require) {
    "use strict";

    var basicFields = require('web.basic_fields');
    var core = require('web.core');
    var abstractField = require('web.AbstractField');
    var widgetRegistry = require('web.field_registry');

    var inputField = basicFields.InputField;

    window.globalImageFieldID = 1;
    var QWeb = core.qweb;
    var _t = core._t;

    function toCamelCase(str) {
        return str
            .replace(/\s(.)/g, function ($1) { return $1.toUpperCase(); })
            .replace(/\s/g, '')
            .replace(/^(.)/, function ($1) { return $1.toLowerCase(); });
    }

    function buildUploader(self, uptoken) {
        self.uploader = Qiniu.uploader({
            runtimes: "html5,flash,html4",
            browse_button: "cy_image_upload_button_" + self.imageFieldID,
            get_new_uptoken: false,
            domain: "https://img.your_domin.com/",
            // uptoken_url: "/uptoken",
            uptoken: uptoken,
            container: "cy_image_field_" + self.imageFieldID,
            max_file_size: "100mb",
            flash_swf_url: "path/of/plupload/Moxie.swf",
            max_retries: 3,
            dragdrop: true,
            drop_element: "cy_image_field_" + self.imageFieldID,
            chunk_size: "4mb",
            auto_start: true,
            init: {
                "FilesAdded": function (up, files) {
                    plupload.each(files, function (file) { });
                },
                "BeforeUpload": function (up, file) {
                    self.$(".cy_image_info").show();
                },
                "UploadProgress": function (up, file) {
                    self.$(".cy_image_info").text("上传中," + file.percent + "%");
                },
                "FileUploaded": function (up, file, info) {
                    var ov = self.value || ''
                    if (self.attrs.widget == "cy_images_field") {
                        ov = '';
                    }
                    var infoObj = JSON.parse(info);
                    jQuery.ajax({
                        url: '/base/imageinfo',
                        type: "GET",
                        dataType: "json",
                        async: false,
                        data: { v: infoObj.key, ov: ov },
                        success: function (data) { }
                    });
                    self.uploadOk(infoObj.key);
                    self.$(".cy_image_info").hide();
                },
                "Error": function (up, err, errTip) { },
                "UploadComplete": function () { },
                "Key": function (up, file) {
                    var nameArr = file.name.split(".");
                    var extName = nameArr[nameArr.length - 1];
                    self.filePath = 'odoo/upload/n' + (0 + Date.now()).toString(36) + '_' + Number(Math.random().toString().substring(2, 10)).toString(36) + '.' + extName;
                    return self.filePath;
                }
            }
        });
    }

    function imageUrl(url, size) {
        if (!size) {
            size = '';
        }
        if (url.includes('https://') || url.includes('http://')) {
            return url;
        }
        return "https://img.your_domin.com/" + url + size;
    }

    var PTImageField = abstractField.extend({
        uploader: null,
        imageFieldID: 0,
        filePath: "",
        events: {
            "click .cy_image_clear_button": function (e) {
                var r = confirm("清除图片会同时清除热区内容！！ \n建议您不要清除图片，直接上传新图片覆盖老图片，这样就可以保留热区了。\n\n点击 “确定” 继续清除，\n点击 “取消” 后可以替换图片。");
                if (!r) { return; }

                var self = this;
                if (self.mode == 'edit') {
                    this._setValue("");
                    this._render();
                }
            },
            "click .cy_image": function (e) {
                var self = this;
                if (self.viewType == "form") {
                    $(".cy_image_marker>img").attr('src', $(e.currentTarget).attr('src'));
                    $(".cy_image_marker").show();
                }
            }
        },
        init: function () {
            var self = this;
            self.imageFieldID = globalImageFieldID++;
            self._super.apply(self, arguments);
            self.set("value", "");
        },
        start: function () {
            var self = this;
            self.display_field();
            return self._super();
        },
        display_field: function () {
            var self = this;

            // console.log(self.mode, self.attrs.hotspots, self.value);

            self.$el.html(QWeb.render("cy_image_field", {
                self: self,
                hotspots: self.mode == 'readonly' && self.attrs.hotspots == 'True' && self.value ? 'True' : ''
            }));
            if (self.mode == 'edit') {
                setTimeout(function () {
                    $.get('/uptoken', function (res) {
                        buildUploader(self, res.uptoken);
                    }, 'json')
                }, 1000)
            }
        },
        _render: function () {
            var self = this;
            self.$('.cy_image_field').addClass(self.viewType);
            var imageSrc = self.value;
            if (imageSrc) {
                if (self.viewType == 'list') {
                    self.$("img").attr("src", imageUrl(imageSrc, '-h36'))
                        .attr('data-source', imageUrl(imageSrc))
                        .addClass('cy_image_field_list_image');
                } else {
                    self.$("img").attr("src", imageUrl(imageSrc, '-h100'))
                        .attr('data-source', imageUrl(imageSrc));
                }
            } else {
                self.$("img").attr("src", "https://img.your_domin.com/static/placeholder.png");
            }
            if (self.mode == 'edit') {
                self.$(".cy_image_field").css("border", "1px solid #CCC").css("padding", "4px");
            } else {
                self.$(".cy_image_field").css("border", "none").css("padding", "0");
            }
        },
        uploadOk: function (url) {
            var self = this;
            self._setValue(url);
            self.$("img").attr("src", url);
        }
    });

    var PTImagesField = abstractField.extend({
        uploader: null,
        imageFieldID: 0,
        filePath: "",
        events: {
            "click .cy_image_clear_button": function (e) {
                var self = this;
                if (self.mode == 'edit') {
                    this._setValue("");
                    this._render();
                }
            },
            "click .cy_image": function (e) {
                var self = this;
                if (self.viewType == "form") {
                    $(".cy_image_marker>img").attr('src', $(e.currentTarget).attr('data-source'));
                    $(".cy_image_marker").show();
                }
            },
            "click .cy_images_item_up": function (e) {
                var self = this;
                var item = $(e.currentTarget).parent().parent('.cy_images_item_div');
                var prevItem = item.prev();
                if (prevItem.length > 0) {
                    item.remove();
                    prevItem.before(item);
                }
                var newValues = [];
                self.$('.cy_images_item_div .cy_image').each(function () {
                    newValues.push($(this).attr('src').replace('https://img.your_domin.com/', ''));
                });
                self._setValue(newValues.join(","));
            },
            "click .cy_images_item_down": function (e) {
                var self = this;
                var item = $(e.currentTarget).parent().parent('.cy_images_item_div');
                var nextItem = item.next();
                if (nextItem.length > 0) {
                    item.remove();
                    nextItem.after(item);
                }
                var newValues = [];
                self.$('.cy_images_item_div .cy_image').each(function () {
                    newValues.push($(this).attr('src').replace('https://img.your_domin.com/', ''));
                });
                self._setValue(newValues.join(","));
            },
            "click .cy_images_item_delete": function (e) {
                var self = this;
                var item = $(e.currentTarget).parent().parent('.cy_images_item_div');
                item.remove();
                var newValues = [];
                self.$('.cy_images_item_div .cy_image').each(function () {
                    newValues.push($(this).attr('src').replace('https://img.your_domin.com/', ''));
                });
                self._setValue(newValues.join(","));
            }
        },
        init: function () {
            var self = this;
            self.imageFieldID = globalImageFieldID++;
            self._super.apply(self, arguments);
            self.set("value", "");
        },
        start: function () {
            var self = this;
            self.display_field();
            return self._super();
        },
        display_field: function () {
            var self = this;
            self.$el.html(QWeb.render("cy_images_field", {
                self: self
            }));
            if (self.mode == 'edit') {
                setTimeout(function () {
                    $.get('/uptoken', function (res) {
                        buildUploader(self, res.uptoken);
                    }, 'json')
                }, 1000)
            }
        },
        _render: function () {
            var self = this;
            self.$('.cy_image_field').addClass(self.viewType);
            var imageSrcs = self.value;
            if (imageSrcs) {
                var imageSrcArr = imageSrcs.split(",");
                var html = '';
                for (var i = 0; i < imageSrcArr.length; i++) {
                    html += '<div class="cy_images_item_div">'
                    if (self.viewType == 'list') {
                        html += '<img class="cy_image cy_image_field_list_image" src="' + imageUrl(imageSrcArr[i], '-h36') + '" data-source="' + imageUrl(imageSrcArr[i]) + '"></img>';
                    } else {
                        html += '<img class="cy_image" src="' + imageUrl(imageSrcArr[i], '-h100') + '" data-source="' + imageUrl(imageSrcArr[i]) + '"></img>'
                    }

                    html += '<div class="cy_images_item_btns">';
                    if (self.mode == 'edit') {
                        html += '<a href="javascript:void(0);" class="cy_images_item_up">前移</a>';
                        html += '<a href="javascript:void(0);" class="cy_images_item_down">后移</a>';
                        html += '<a href="javascript:void(0);" class="cy_images_item_delete">删除</a>';
                    }
                    if (self.mode == 'readonly' && self.attrs.hotspots == 'True' && self.value ? 'True' : '') {
                        html += '<a class="cy_images_hotspots_button" target="_blank" href="/cy_base/static/src/html/hotspot.html?v=' + imageSrcArr[i] + '">画热区</a>';
                    }
                    html += '</div></div>';
                }
                self.$(".cy_images_field_content").html(html);
            } else {
                self.$(".cy_images_field_content").html('<div><img src="https://img.your_domin.com/static/placeholder.png"></img></div>');
            }
        },
        uploadOk: function (url) {
            var self = this;
            var imageSrcs = self.value;
            if (imageSrcs) {
                imageSrcs = imageSrcs + "," + url;
            } else {
                imageSrcs = url;
            }
            self._setValue(imageSrcs);
            self._render();
        }
    });

    var AdvancedHtmlWidget = inputField.extend({
        className: 'oe_form_field oe_form_field_html_text',
        supportedFieldTypes: ['text', 'html'],
        init: function () {
            this._super.apply(this, arguments);
            this.tagName = 'div';
        },
        _initClipboard: function () {
            var self = this;
            this.$('.o_clipboard_button').each(function () {
                var $button = $(this);
                $button.tooltip({ title: _t('Copied !'), trigger: 'manual', placement: 'right' });
                this.clipboard = new ClipboardJS($button[0], {
                    text: function () {
                        return $button.attr('text').trim();
                    },
                    container: self.$el[0]
                });
                this.clipboard.on('success', function () {
                    _.defer(function () {
                        $button.tooltip('show');
                        _.delay(function () {
                            $button.tooltip('hide');
                        }, 800);
                    });
                });
            });
        },
        _initIframe: function () {
            var self = this;
            this.$('.o_iframe_button').each(function () {
                var $button = $(this);
                $button.on('click', function () {
                    var iframeURL = $button.attr('url');
                    var popDiv = $(`<div style="position: fixed;height:100vh;width:100vw;top:0;left:0;background:rgba(0,0,0,0.5);">
                        <div style="position: fixed;height: 80vh;width: 80vw;top:10vh;left:10vw;background: #FFF;">
                            <iframe width="100%" height="100%" src="${iframeURL}"></iframe>
                            <div style="position: fixed;bottom: 10vh;right: 10vw;margin:8px 16px;">
                                <button class="o_iframe_button_save btn btn-primary ">确定</button>
                                <button class="o_iframe_button_close btn " style="margin-left:6px;">关闭</button>
                            </div>
                        </div>
                    </div>`);
                    $('body').append(popDiv)
                    popDiv.find('.o_iframe_button_close').on('click', function () {
                        popDiv.remove()
                    });
                    popDiv.find('.o_iframe_button_save').on('click', function () {
                        var iframe = popDiv.find("iframe").get(0);
                        iframe.contentWindow.do_save();

                        self.__parentedParent.__parentedParent.reload()
                        popDiv.remove()
                    });
                });
            });
        },
        _render: function () {
            this.$el.html(this.value);
            this._initClipboard();
            this._initIframe();
        }
    });

    var AdvancedUrlWidget = inputField.extend({
        className: 'o_field_url',
        events: _.extend({}, inputField.prototype.events, {
            'click': '_onClick',
        }),
        supportedFieldTypes: ['char'],

        init: function () {
            this._super.apply(this, arguments);
            this.tagName = this.mode === 'readonly' ? 'div' : 'input';
        },
        _initClipboard: function () {
            var self = this;
            var $clipboardBtn = this.$('.o_clipboard_button');
            $clipboardBtn.tooltip({ title: _t('Copied !'), trigger: 'manual', placement: 'right' });
            this.clipboard = new ClipboardJS($clipboardBtn[0], {
                text: function () {
                    return self.value.trim();
                },
                container: self.$el[0]
            });
            this.clipboard.on('success', function () {
                _.defer(function () {
                    $clipboardBtn.tooltip('show');
                    _.delay(function () {
                        $clipboardBtn.tooltip('hide');
                    }, 800);
                });
            });
        },
        getFocusableElement: function () {
            return this.mode === 'readonly' ? this.$el : this._super.apply(this, arguments);
        },

        _renderReadonly: function () {
            var self = this;
            var keys = (this.attrs.keys || '').split(',');
            var url = this.attrs.url;
            keys.forEach(function (key) {
                url = url.replace('{{' + key + '}}', self.recordData[key])
            });
            var text = this.attrs.text || this.value;
            this.$el.css('display', 'flex');
            this.$el.html('<a name="order_no" style="margin-right: 20px;" target="_blank" href="' + url + '">' + text + '</a><button class="btn btn-secondary o_clipboard_button">复制</button>');
            this._initClipboard();
        },

        _onClick: function (ev) {
            ev.stopPropagation();
        },
    });


    var CheckboxString = abstractField.extend({
        events: {
            "change .cbsf": function (e) {
                var self = this;
                var datas = [];
                self.$(".cbsf").each(function () {
                    if ($(this).prop("checked")) {
                        datas.push($(this).attr("value"));
                    }
                });
                self._setValue(datas.join(","));
            }
        },
        init: function () {
            var self = this;
            self._super.apply(self, arguments);
            self.set("value", "");
        },
        start: function () {
            var self = this;
            self.display_field();
            return self._super();
        },
        display_field: function () {
            var self = this;
            self.$el.html(QWeb.render("checkbox_string_field", {
                self: self,
                datas: eval(self.attrs.checkbox_data)
            }));
        },
        _render: function () {
            var self = this;
            if (self.mode == 'edit') {
                self.$(".cbsf").prop("disabled", false);
            } else {
                self.$(".cbsf").prop("disabled", true);
            }
            var value = self.value;
            self.$(".cbsf").prop("checked", false);
            if (value) {
                var datas = value.split(",");
                for (var i = 0; i < datas.length; i++) {
                    self.$(".cbsf_" + datas[i]).prop("checked", true);
                }
            }
        }
    });

    var PTProductList = abstractField.extend({
        controller: {},
        activeId: 1,
        context: {},
        html: `<table class="product-list-table" style="width:100%;border:1px solid black;table-layout:fixed;" border="1"   cellspacing="0">
       <tr>
            <th>
                ID
            </th>
            <th>
                SN
            </th>
            <th>
                图片
            </th>
            <th>
                售价
            </th>
            <th>
                市场价格
            </th>
            <th>
                活动
            </th>
        </tr> 
        {{~it:value:index}}
            <tr>
                <td>
                    {{=it[index].id}}
                </td>
                <td>
                    {{=it[index].sn}}
                </td>
                <td>
                    <img src="{{= it[index].image}}" style="width:60px;height:60px">
                </td>
                <td>
                    {{=it[index].shopPrice}}
                </td>
                <td>
                    {{=it[index].marketPrice}}
                </td>
                <td>
                    {{? it[index].isFlashsale}}
                        Flashsale
                    {{??}}
                        -
                    {{?}}
                </td>
            </tr>
        {{~}}
    </table>`,
        init() {
            this._super.apply(this, arguments);
        },
        start() {
            console.log(this)
            this.display_field();
            return this._super();
        },
        display_field() {
            this.$el.html(QWeb.render("cy-product-list", { self: this }));
        },
        _render() {
            if (this.value) {
                var self = this
                var container = this.$el.find(".product-table-pagination")
                container.pagination({
                    dataSource: "/base/condition-skcs",
                    pageSize: 100,
                    locator: "data.list",
                    totalNumberLocator: function (response) {
                        console.log(response)
                        if (response.data) {
                            return response.data.total
                        }
                        return 0
                    },
                    callback: function (data, pagination) {
                        // template method of yourself
                        self.showTable(data)
                    },
                    ajax: {
                        type: "POST",
                        dataType: "json",
                        data: {
                            "conditionId": self.value,
                        },
                    },
                    alias: {
                        pageNumber: 'page',
                        pageSize: 'size'
                    }
                })
            }
        },
        showTable(data) {
            var container = this.$el.find(".product-table")
            var fn = doT.template(this.html)
            var c = fn(data)
            container.html(c)
        }
    })

    var PTQueryBuilder = abstractField.extend({
        rules_basic: {},
        categorys: [],
        colors: [],
        sizes: [],
        events: {
            "click #save-btn": function () {
                var res = this.br.queryBuilder("getRules")
                console.log("commit ", res)
                if (res) {
                    this._setValue(JSON.stringify(res))
                    this.do_notify(_t("Success"), _t("保存成功"));
                    this.$el.find(".cy-qbuilder-container").addClass("cy-hide")
                } else {
                    this.do_warn(_t("Error"), _t("表达式错误"));
                }
            },
            "click #edit-btn": function () {
                this.$el.find(".cy-hide").removeClass("cy-hide")
            },
            "click #cancel-btn": function () {
                this.$el.find(".cy-qbuilder-container").addClass("cy-hide")
            }
        },
        getCategorys() {
            var self = this
            jQuery.ajax({
                url: '/base/categories',
                type: "GET",
                dataType: "json",
                async: false,
                data: { v: new Date().getTime() },
                success: function (data) {
                    self.categorys = data;
                }
            });
            jQuery.ajax({
                url: '/base/colors-sizes',
                type: "GET",
                dataType: "json",
                async: false,
                data: { v: new Date().getTime() },
                success: function (data) {
                    self.colors = data.colors;
                    self.sizes = data.sizes;
                }
            });
            console.log("==", this.categorys);
        },
        init() {
            console.log(this)
            this._super.apply(this, arguments);
            this.set("value", "");
            this.getCategorys();
        },
        start() {
            console.log(this)
            this.display_field();
            return this._super();
        },
        display_field() {
            this.$el.html(QWeb.render("query_builder", { self: this }));
        },
        _render() {
            this.display_qbuilder(this.categorys, this.colors)
            this.$el.find("#condition").html(this.value)
            if (this.mode == 'edit') {
                this.$el.find("#edit-btn").removeClass("cy-hide")
            } else {
                this.$el.find("#edit-btn").addClass("cy-hide")
            }
        },
        display_qbuilder(cats, colors) {
            this.br = this.$el.find("#builder")
            var filter = [{
                id: 'name',
                field: "name",
                label: '商品名称',
                type: 'string',
                operators: ['contains', 'not_contains']
            },
            {
                id: 'price',
                field: 'price',
                label: '价格',
                type: 'double',
                validation: {
                    min: 0,
                    step: 0.01
                },
                operators: ['between', 'not_between']
            },
            {
                id: 'firstShelfTime',
                field: 'firstShelfTime',
                label: '首次上架时间',
                type: 'double',
                validation: {
                    min: 0,
                    step: 0.01
                },
                operators: ['greater', 'greater_or_equal', 'less', 'less_or_equal']
            },
            {
                id: 'belongCates',
                label: '分类',
                field: 'belongCates',
                type: 'integer',
                selection: new CategorySelector({}),
                cate: 0,
                input(rule, name) {
                    var container = rule.$el.find(".rule-value-container")
                    var classid = name + "_categories"
                    this.selection = new CategorySelector({
                        "el": container,
                        "id": classid,
                        "data": cats,
                        "selName": "categorys",
                        "value": [], // 初始化数据 [1, 3, 6] 分别为每个区域ID
                        "text": ["选择分类"],
                    })
                    container.on("change", "select", this.selection.onchange())
                    return "<div class=\"" + classid + "\">" + this.selection.update([0]) + "</div>"
                },
                valueSetter(rule, value) {
                    var vals = this.selection.getParentClass(value)
                    console.log("value setter", vals)
                    this.selection.update(vals)
                },
                valueGetter(rule) {
                    var val = 0
                    var container = rule.$el.find(".rule-value-container")
                    container.find("select").each(function () {
                        if (this.value == 0) {
                            return
                        }
                        val = parseInt(this.value)
                    })
                    console.log("value getter", val)
                    return val
                },
                operators: ['equal', 'not_equal']
            },
            {
                id: 'containColors',
                label: '颜色',
                field: 'containColors',
                type: 'integer',
                selection: new CategorySelector({}),
                cate: 0,
                input(rule, name) {
                    var container = rule.$el.find(".rule-value-container")
                    var classid = name + "_categories"
                    this.selection = new CategorySelector({
                        "el": container,
                        "id": classid,
                        "data": colors,
                        "selName": "categorys",
                        "value": [], // 初始化数据 [1, 3, 6] 分别为每个区域ID
                        "text": ["选择颜色"],
                    })
                    container.on("change", "select", this.selection.onchange())
                    return "<div class=\"" + classid + "\">" + this.selection.update([0]) + "</div>"
                },
                valueSetter(rule, value) {
                    var vals = this.selection.getParentClass(value)
                    console.log("value setter", vals)
                    this.selection.update(vals)
                },
                valueGetter(rule) {
                    var val = 0
                    var container = rule.$el.find(".rule-value-container")
                    container.find("select").each(function () {
                        if (this.value == 0) {
                            return
                        }
                        val = parseInt(this.value)
                    })
                    console.log("value getter", val)
                    return val
                },
                operators: ['equal', 'not_equal']
            },
            {
                id: "skcSn",
                field: "skcSn",
                label: "货号",
                type: "string",
                operators: ['in', 'not_in'],
                input: function (rule) {
                    return '<textarea id="product_sn" name="w3review" rows="4" cols="30">'
                },
                valueGetter: function (rule, name) {
                    var sns = rule.$el.find("#product_sn").val().split(/\r?\n/).filter(sn => {
                        sn = sn.replace(/^\s+|\s+$/gm, '')
                        if (sn.length <= 0) {
                            return false
                        }
                        return true
                    });
                    if (sns.length <= 0) {
                        return ""
                    }
                    return sns
                },
                valueSetter: function (rule, value) {
                    console.log("sssssster", value)
                    if (value.length <= 0) {
                        value = [""]
                    }
                    var v = value.join("\n")
                    rule.$el.find("#product_sn").val(v)
                }
            }
            ]

            if (this.sizes.length > 0) {
                var f = {
                    id: 'size',
                    label: '尺寸',
                    field: "size",
                    type: 'integer',
                    input: 'checkbox',
                    values: {}
                }
                this.sizes.forEach(c => {
                    f.values[c.id] = c.name
                });
                filter.push(f)
            }

            this.br.queryBuilder({
                filters: filter,
            })
            try {
                if (this.value.length > 0) {
                    var res = JSON.parse(this.value)
                    console.log(this.value)
                    this.br.queryBuilder("setRules", res)
                }
            } catch (e) {
                console.log(e)
                this.do_warn(_t("Error"), _t("表达式错误"));
            }
            this.br.addClass("cy-fullscreen")
            // br.on('rulesChanged.queryBuilder',function(e,rule){
            // })
        }
    })

    var PtInput = abstractField.extend({
        events: {
            "click": "showInput",
            "focusout": "save"
        },
        className: "o_field_input",
        init() {
            this._super.apply(this, arguments);
        },
        start() {
            this.display_field();
            return this._super();
        },
        display_field() {
            this.$el.html(QWeb.render("integer_input", { self: this }));
        },
        _render() {
            this.$el.find(".cy-input-edit").addClass("cy-hide").val(this.value)
            this.$el.find(".cy-input-show").removeClass("cy-hide").html(this.value)
        },
        showInput(event) {
            event.stopPropagation()
            this.$el.find(".cy-input-edit").removeClass("cy-hide")
            this.$el.find(".cy-input-show").addClass("cy-hide")
        },
        save(ev) {
            var value = this.$el.find(".cy-input-edit").val()
            console.log(value)
            this._setValue(value, {
                doNotSetDirty: true
            })
        }
    })

    widgetRegistry.add('cy_query_builder', PTQueryBuilder);
    widgetRegistry.add('cy_image_field', PTImageField);
    widgetRegistry.add("cy_images_field", PTImagesField);
    widgetRegistry.add('advanced_url', AdvancedUrlWidget);
    widgetRegistry.add('advanced_html', AdvancedHtmlWidget);
    widgetRegistry.add("checkbox_string", CheckboxString);
    widgetRegistry.add('cy_input', PtInput);
    widgetRegistry.add('cy_product_list', PTProductList);



    var AbstractAction = require('web.AbstractAction');
    var PageFrameAction = AbstractAction.extend({
        template: 'page_frame_widget',
        init: function (parent, context) {
            this._super(parent, context);
            this.context = context.context
            this.active_id = this.context.active_id;
            console.log(this.active_id)
            this.frame_url = this.active_id == undefined ? context.params.url : context.params.url + "?id=" + this.active_id;
            this.frame_full = context.params.full || false;
        },
        start: function () {
            this.load_fn();
        },
        destroy: function () {
            var self = this;
            if (self.frame_full) {
                self.$el.attr('style', '');
            }
            this._super();
        },
        events: {
            "click .page_frame_iframe_refresh_button": function (e) {
                var self = this;
                self.$el.find('.page_frame_iframe').attr('src', self.frame_url + '?_=' + (new Date()).getTime());
            }
        },
        load_fn: function () {
            var self = this;
            // self.$el.find('.page_frame_iframe_refresh_button').attr('href', self.frame_url + '?_=' + (new Date()).getTime());
            self.$el.find('.page_frame_iframe').attr('src', self.frame_url + '?_=' + (new Date()).getTime());
            if (self.frame_full) {
                self.$el.attr('style', 'position: fixed;');
            }
        }
    });
    core.action_registry.add('cy.page_frame.wizard_tag', PageFrameAction);

    return {
        PTImageField: PTImageField,
        PTImagesField: PTImagesField,
        AdvancedUrlWidget: AdvancedUrlWidget,
        AdvancedHtmlWidget: AdvancedHtmlWidget,
        CheckboxString: CheckboxString,
        PageFrameAction: PageFrameAction,
        PTQueryBuilder: PTQueryBuilder,
        PtInput: PtInput
    }

});

$(function () {
    $('body').append('<div class="cy_image_marker"><img src="https://img.your_domin.com/static/placeholder.png"></img></div><svg id="cy_image_field_list_image_arraw"><path d="M0 15 L30 0 L30 30 Z"/></path></svg><div id="cy_image_field_list_image_tips"><img src="https://img.your_domin.com/static/placeholder.png"></img></div>');
    var listMouseoverY = 0;
    var listOrgImage = null;
    $(document).on('mouseover', '.cy_image_field_list_image', function (e) {
        $("#cy_image_field_list_image_tips>img").attr('src', $(this).attr('data-source'));
        listMouseoverY = e.pageY;
        listOrgImage = $(this);
        e.stopPropagation();
    });
    var hotspotsCache = {};
    function drawHotspotsByUrl(imageURL) {
        var hc = hotspotsCache[imageURL];
        var ts = (new Date()).getTime() / 1000;
        if (hc && hc.ts > ts - 60) {
            drawHotspots(hc.data);
            return;
        }
        $.post('/base/load_hotspots', { v: imageURL }, function (res) {
            hotspotsCache[imageURL] = { ts: ts, data: res };
            drawHotspots(res);
        }, 'json');
    }
    function drawHotspots(hotspots) {
        var tips = $("#cy_image_field_list_image_tips");
        tips.find('div').remove()
        if (!hotspots || hotspots.length == 0) {
            return
        }

        var tipsImg = $("#cy_image_field_list_image_tips>img");
        var tipsHeight = tipsImg.height();
        var tipsWidth = tipsImg.width();
        var tipsOrgHeight = tipsImg.get(0).naturalHeight;
        var tipsOrgWidth = tipsImg.get(0).naturalWidth;


        for (var i = 0; i < hotspots.length; i++) {
            var hotspot = hotspots[i];
            var hsTop = hotspot.y * tipsHeight / tipsOrgHeight;
            var hsLeft = hotspot.x * tipsWidth / tipsOrgWidth;
            var hsHeight = hotspot.h * tipsHeight / tipsOrgHeight;
            var hsWidth = hotspot.w * tipsWidth / tipsOrgWidth;

            if (hsTop < 0) { hsHeight += hsTop; hsTop = 0; }
            if (hsLeft < 0) { hsWidth += hsLeft; hsLeft = 0; }

            tips.append(`<div style="position:absolute;top:${hsTop}px;left:${hsLeft}px;width:${hsWidth}px;height:${hsHeight}px;">${hotspot.name}</div>`)
        }
    }
    $("#cy_image_field_list_image_tips>img").on('load', function () {
        if (!listMouseoverY || !listOrgImage) return;
        var tipsImg = $(this);
        var tips = tipsImg.parent();
        var win = $(window);
        var tipsHeight = tips.height();
        var moveTop = listMouseoverY - tipsHeight / 2;
        if (moveTop + tipsHeight > win.outerHeight()) {
            moveTop = win.outerHeight() - tipsHeight - 8;
        } else if (moveTop < 0) {
            moveTop = 5;
        }
        var offsetObj = listOrgImage.offset();
        var moveLeft = offsetObj.left + listOrgImage.width() + 20;
        tips.css('top', moveTop).css('left', moveLeft).show();
        $("#cy_image_field_list_image_arraw").css('top', offsetObj.top + 4).css('left', moveLeft - 26).show();
        drawHotspotsByUrl(new URL(tipsImg.attr('src')).pathname.substring(1));
    });
    $(document).on('mouseout', '.cy_image_field_list_image', function (e) {
        $("#cy_image_field_list_image_tips").hide();
        $("#cy_image_field_list_image_arraw").hide();
        e.stopPropagation();
    });
    $(document).on('mousemove', '.cy_image_field_list_image', function (e) {
        e.stopPropagation();
    });
    $(document).on('mousemove', function (e) {
        $("#cy_image_field_list_image_tips").hide();
        $("#cy_image_field_list_image_arraw").hide();
    });
    $(".cy_image_marker").on('click', function () {
        $(this).hide();
    });

    function titleModified() {
        if (document.title.indexOf('Odoo') != -1) {
            document.title = document.title.replace('Odoo', 'CY Store')
        }
    }

    titleModified();
    var titleEl = document.getElementsByTagName("title")[0];
    var docEl = document.documentElement;
    if (docEl && docEl.addEventListener) {
        docEl.addEventListener("DOMSubtreeModified", function (evt) {
            var t = evt.target;
            if (t === titleEl || (t.parentNode && t.parentNode === titleEl)) {
                titleModified();
            }
        }, false);
    } else {
        document.onpropertychange = function () {
            if (window.event.propertyName == "title") {
                titleModified();
            }
        };
    }
});