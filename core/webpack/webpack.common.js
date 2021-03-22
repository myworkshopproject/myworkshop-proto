const path = require('path');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const BundleTracker = require('webpack-bundle-tracker');
const { WebpackManifestPlugin } = require('webpack-manifest-plugin');

module.exports = {
    entry: {
        base: './src/base.js',
        home: './src/home.js',
    },
    plugins: [
        new CleanWebpackPlugin(),
        new MiniCssExtractPlugin({
            filename: 'css/[name].[contenthash].css',
            chunkFilename: 'css/[name].[contenthash].css',
        }),
        new BundleTracker({
            filename: 'webpack-stats.json',
        }),
        new WebpackManifestPlugin()
    ],
    output: {
        filename: 'js/[name].[contenthash].js',
        path: path.resolve(__dirname, '../dist/assets'),
        publicPath: '/assets/',
    },
    optimization: {
        moduleIds: 'deterministic',
        runtimeChunk: 'single',
        splitChunks: {
            cacheGroups: {
                vendor: {
                    test: /[\\/]node_modules[\\/]/,
                    name: 'vendors',
                    chunks: 'all',
                },
            },
        },
    },
    module: {
        rules: [{
                test: /\.elm$/i,
                exclude: [/elm-stuff/, /node_modules/],
                use: {
                    loader: "elm-webpack-loader",
                    options: {}
                },
            },
            {
                test: /\.css$/i,
                use: [MiniCssExtractPlugin.loader, 'css-loader'],
            },
            {
                test: /\.s[ac]ss$/i,
                use: [MiniCssExtractPlugin.loader, 'css-loader', 'sass-loader'],
            },
            {
                test: /\.(png|svg|jpg|jpeg|gif)$/i,
                use: {
                    loader: "file-loader",
                    options: {
                        name: 'img/[contenthash].[ext]',
                    },
                },
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/i,
                use: {
                    loader: "file-loader",
                    options: {
                        name: 'fonts/[contenthash].[ext]',
                    },
                },
            },
        ],
    },
};
