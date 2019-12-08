<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

class AlterAnalyzersTable extends Migration
{
    /**
     * Run the migrations.
     *
     * @return void
     */
    public function up()
    {
        Schema::table('analizers', function (Blueprint $table) {
            $table->string("module")->nullable()->after('active');
            $table->string("classname")->nullable()->after('active');
            $table->dropColumn('script');            
        });
    }

    /**
     * Reverse the migrations.
     *
     * @return void
     */
    public function down()
    {
        Schema::table('analyzers', function (Blueprint $table) {
            //
        });
    }
}
