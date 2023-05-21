var utils = {
    callbacks: [],
    _showTimeout: null,
    _showLoading(isShow) {
        if (!!this._showTimeout) {
            clearTimeout(this._showTimeout);
            this._showTimeout = null;
        }
        var loading_ele = document.getElementById('loading_div');
        if (!loading_ele) {
            var e = document.createElement('div');
            e.innerHTML = `<div id="loading_div" style="position:fixed;top: 0;bottom: 0;left: 0;right: 0;background-color: rgba(0,0,0,0.1);z-index:10000;display:none;">
<div style="background-color: rgba(0,0,0,0.7);margin: auto;width: 240px;height:90px;margin-top: 300px;border-radius:10px;">
<img style="width: 83px;margin: auto;display: block;" src="../images/loading.gif"></div></div>`;
            document.body.appendChild(e);
            loading_ele = document.getElementById('loading_div');
            if (!loading_ele) return;
        };
        if (isShow) {
            loading_ele.style.display = 'block';
            this._showTimeout = setTimeout(() => {
                this._showTimeout = null;
                loading_ele.style.display = 'none';
            }, 10000);
        } else {
            loading_ele.style.display = 'none';
        }
    },
    addCallback(f) {
        this.callbacks.push(f);
    },
    runCallbacks() {
        for (var i = 0; i < this.callbacks.length; i++) {
            var f = this.callbacks[i];
            if (!!f) {
                f();
            }
        }
    },
    init() {
        axios.interceptors.request.use((config) => {
            if (config.loading) {
                utils._showLoading(true);
            }
            return config;
        }, (error) => {
            return Promise.reject(error);
        });
        axios.interceptors.response.use((response) => {
            utils._showLoading(false);
            return response;
        }, (error) => {
            return Promise.reject(error);
        });


        axios.get('/base/api_host', {}, { loading: true }).then((response) => {
            var apiHost = response.data;
            // api_axios is api host
            window.api_axios = axios.create({ baseURL: '//' + apiHost })
            // Add a request interceptor
            api_axios.interceptors.request.use((config) => {
                if (config.loading) {
                    utils._showLoading(true);
                }
                return config;
            }, (error) => {
                return Promise.reject(error);
            });
            api_axios.interceptors.response.use((response) => {
                utils._showLoading(false);
                return response;
            }, (error) => {
                return Promise.reject(error);
            });

            this.runCallbacks();
        });
    }
};


utils.init()