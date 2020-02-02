<?php

Route::resource('noticias','NoticiasController');

Route::get('/', 'NoticiasController@index')->name('home');

Route::get('/noticias/{id}/confirm','NoticiasController@confirm')->name('noticias.confirm');

Route::post('/noticias/favorite','NoticiasController@favorite')->name('noticias.favorite');

Route::post('/noticias/settags','NoticiasController@settags')->name('noticias.settags');

Route::post('/noticias/gettags','NoticiasController@gettags')->name('noticias.gettags');

Route::post('/noticias/markread','NoticiasController@markread')->name('noticias.markread');

Route::post('/noticias/delete','NoticiasController@delete')->name('noticias.delete');

//Route::get('/noticias/datos','NoticiasController@datos')->name('noticias.datos');
Route::get('/news/datos','NoticiasController@datos');

Route::resource('analisis','AnalisisController');

Route::get('/analizadores','AnalizerController@index')->name('analizers.index');

Route::get('/analizadores/edit','AnalizerController@edit')->name('analizers.edit');

Route::get('/analizadores/destroy','AnalizerController@edit')->name('analizers.destroy');

Route::get('analysis','AnalisisController@ajax')->name('analysis');