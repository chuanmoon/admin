function CategorySelector(options = {}) {
    this.options = {
        "el": {},
        "text": ["选择分类"], // 默认 option 文本
        "id": "",
        "value": [], // 当前选中值 value = [1,2,3]
        "data": [], // 分类数据对象
        "selName": "sel", // select 表单名称
        "className": [], // 分类名称
        "obj": null, // 实例化对象名称
    };

    // 合并对象
    if (options) {
        Object.assign(this.options, options)
    }
}

CategorySelector.prototype = {
    constructor: CategorySelector,

    update(classId) {
        this.options.value = [...classId]
            // 浅拷贝，禁止对象引用
        let _classid = Object.assign([], classId)

        // 数组首位插入一个0值，由于获取分类数据是按topid来的
        _classid.unshift(0)

        let [html, selName] = ["", this.options.selName];

        for (let [key, cid] of _classid.entries()) {
            let newClass = this.getClass(cid);
            if (newClass.length > 0) {
                let name = selName + "_" + key + "_ST";
                const option = this.options.text[key] || this.options.text[0];

                html += '<select name="' + name + '" key="' + key + '"  class="form-control">';
                html += '<option value="0">' + option + '</option>';
                if (newClass) {
                    for (let value of newClass) {
                        if (value[1] == this.options.value[key]) {
                            html += '<option value=' + value[1] + ' selected>' + value[2] + '</option>';
                        } else {
                            html += '<option value=' + value[1] + '>' + value[2] + '</option>';
                        }
                    }
                }
                html += '</select>';
            }
        }
        if (this.options.el) {
            this.options.el.find("." + this.options.id).html(html)
        }
        return html
    },
    onchange() {
        var self = this
        return function(e) {
            var key = $(this).attr("key")
            var value = $(this).val()
            self.setClass(parseInt(value), this.options[this.selectedIndex].text, parseInt(key))
            self.options.el.trigger("change")
        }
    },
    // 更新
    setClass(value, text, key) {
        let [val, name] = [this.options.value, this.options.className];
        val[key] = parseInt(value);
        name[key] = text;

        // 大于0，需预留下级数据字段，小于0，则清除下级数据
        if (value > 0) {
            key++;
        }

        // 清除数据
        val.splice(key);
        name.splice(key);

        // 更新
        this.update(val)
    },
    // 根据topid获取分类数据
    getClass(topId) {
        return this.options.data.filter(item => {
            if (item[0] == topId) {
                return item;
            }
        })
    },
    getParentClass(id) {
        if (id == 0) {
            return []
        }
        var self = this
        var list = []
        this.options.data.forEach(item => {
            if (item[1] == id) {
                console.log('find parent', item[0])
                l = self.getParentClass(item[0])
                list = list.concat(l)
            }
        });
        list.push(id)
        return list
    },
    getAllChilren(id) {
        var self = this
        var list = [id]
        this.options.data.forEach(e => {
            if (e[0] == id) {
                var x = self.getAllChilren(e[1])
                list = list.concat(x)
            }
        })
        return list
    }
}