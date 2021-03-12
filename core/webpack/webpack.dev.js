const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');
const HtmlWebpackPlugin = require('html-webpack-plugin');
var path = require('path');

module.exports = merge(common, {
    mode: 'development',
    output: {
        publicPath: '/',
    },
    devtool: 'inline-source-map',
    devServer: {
        contentBase: path.join(__dirname, 'assets'),
        inline: true,
        stats: 'errors-only',
    },
    plugins: [
        new HtmlWebpackPlugin({
            title: 'development',
            template: 'src/index.html',
        }),
    ],
});
