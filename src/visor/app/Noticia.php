<?php

namespace App;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Support\Facades\DB;

class Noticia extends Model
{
    public function scopeBuscar($query, $bulletin,$bulletin_year, $bulletin_no,$destacado,$tag,$sdate)
    {
        $conditions = [];
        $query->select('noticias.id','bulletin','bulletin_year','bulletin_no','seccion','organismo','organo','bulletin_date','organization','newname','url','fav','notify','readed','noticias.created_at','noticias.updated_at');

        if ($bulletin && $bulletin <> "Boletín")
        {
            $conditions[] = ['bulletin', 'LIKE', "%$bulletin%"];
        }
        if ($bulletin_year && $bulletin_year <> "Año")
        {
            $conditions[] = ['bulletin_year', '=', $bulletin_year];
        }
        if ($bulletin_no)
        {
            $conditions[] = ['bulletin_no', '=', $bulletin_no];
        }
        if ($destacado == "Destacados")
        {
            $conditions[] = ['fav', '=', 1];
        }
        if ($destacado == "No Destacados")
        {
            $conditions[] = ['fav', '=', 0];
        }

        if ($sdate)
        {
            $conditions[] = ['bulletin_date', '=', "$sdate"];
        }

        if ($tag && $tag <> 'Etiquetas')
        {
            $query->join('noticia_tag', 'noticias.id', '=', 'noticia_id');
            $conditions[] = ['tag_id','=',$tag];
        }

        return $query->where($conditions)->orderBy('bulletin_date', 'DESC')->paginate(10);
    }    

    // relaciones
    public function tags()
    {
        return $this->belongsToMany('\App\Tag')->withTimestamps();
    }    

    public static function getTagsByNewId($ids)
    {
        $tmp_i = [];
        $tmp_f = [];

        foreach ($ids as $id)
        {
            $tmp = DB::table('noticia_tag')->select('tag_id')->where('noticia_id','=',$id)->get();    
            $tmp_i = [];
            if (count($tmp) == 0)
                return $tmp_f;
            foreach ($tmp as $item)
            {
                $tmp_i [] = $item->tag_id;
            } 
            if (count($tmp_f) == 0)
                foreach ($tmp_i as $i)
                    $tmp_f [] = $i;
            else 
                $tmp_f = array_intersect($tmp_f, $tmp_i);
        }

        return ($tmp_f);
    }

}
