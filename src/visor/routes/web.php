<?php

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|

Route::get('/', function () {
    return view('welcome');
});
*/

Route::resource('noticias','NoticiasController');

Route::get('/', 'NoticiasController@index')->name('home');

Route::get('/noticias/{id}/confirm','NoticiasController@confirm')->name('noticias.confirm');

Route::post('/noticias/favorite','NoticiasController@favorite')->name('noticias.favorite');

Route::post('/noticias/settags','NoticiasController@settags')->name('noticias.settags');

Route::post('/noticias/gettags','NoticiasController@gettags')->name('noticias.gettags');

Route::post('/noticias/markread','NoticiasController@markread')->name('noticias.markread');

Route::post('/noticias/delete','NoticiasController@delete')->name('noticias.delete');

Route::post('/noticias/datos','NoticiasController@datos')->name('noticias.datos');

Route::resource('analisis','AnalisisController');

Route::get('/analizadores','AnalizerController@index')->name('analizers.index');

Route::get('/analizadores/edit','AnalizerController@edit')->name('analizers.edit');

Route::get('/analizadores/destroy','AnalizerController@edit')->name('analizers.destroy');
