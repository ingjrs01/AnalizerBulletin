<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class CreateNoticiasTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::create('noticias', function (Blueprint $table) {
            $table->bigIncrements('id');
            $table->string('bulletin',20);
            $table->smallInteger('bulletin_year');
            $table->integer('bulletin_no');
            $table->date('bulletin_date');
            $table->string('organization',150);
            $table->string('newname',1000);
            $table->string('url',250);
            $table->boolean('fav');
            $table->boolean('notify');
            $table->boolean('readed');
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::dropIfExists('noticias');
    }
}
