<?php
use App\Http\Middleware\Cors;

Route::resource('noticias','NoticiasController');

//Route::group(['middleware' => ['cors']], function () {
    //Rutas a las que se permitirá acceso
    Route::get('/', 'NoticiasController@index')->name('home');
//});
//Route::get('/',['middleware' => 'cors','NoticiasController@index' ])->name('home');
Route::get('/api/noticias',function(){
    return json_encode(["resultados"]);
});
Route::get('/noticias/{id}/confirm','NoticiasController@confirm')->name('noticias.confirm');
Route::post('/noticias/favorite','NoticiasController@favorite')->name('noticias.favorite');
Route::post('/noticias/settags','NoticiasController@settags')->name('noticias.settags');
Route::post('/noticias/gettags','NoticiasController@gettags')->name('noticias.gettags');
Route::post('/noticias/markread','NoticiasController@markread')->name('noticias.markread');
Route::post('/noticias/delete','NoticiasController@delete')->name('noticias.delete');
Route::post('/noticias/datos','NoticiasController@datos')->name('noticias.datos');
Route::get('/news/datos','NoticiasController@ajax');
Route::resource('analisis','AnalisisController');
Route::get('/analizadores','AnalizerController@index')->name('analizers.index');
Route::get('/analizadores/edit','AnalizerController@edit')->name('analizers.edit');
Route::get('/analizadores/destroy','AnalizerController@edit')->name('analizers.destroy');
Route::get('/analizadores/ajax','AnalizerController@ajax')->name('analizers.ajax');
Route::post('analizadores/state','AnalizerController@state')->name('analizers.state');
Route::post('analizadores/save','AnalizerController@save')->name('analizers.save');
Route::post('analizadores/delete','AnalizerController@delete')->name('analizers.delete');
Route::get('analysis','AnalisisController@ajax')->name('analysis');
