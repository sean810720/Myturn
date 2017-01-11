<?php
defined('BASEPATH') or exit('No direct script access allowed');

/**
 *   名稱:    範例頁面
 *   路徑:    controllers/Test
 *   開發者:  Sean@2016/12/19
 *   網址:    http://{Domain Name}/test
 */

class Test extends CI_Controller
{
    /*
    |--------------------------------------------------------------------------
    | 頁面查詢條件屬性
    |--------------------------------------------------------------------------
     */
    private $query = array(

        // WHERE 條件
        'where' => array(),

        // 搜尋關鍵字
        'keyword' => '',

        // 排序
        'by' => array(),
    );

    /*
    |--------------------------------------------------------------------------
    | 範例頁面 - 列表
    |--------------------------------------------------------------------------
    |
    | 呼叫路徑: http://{Domain Name}/demo/index
    | 呼叫方式: 無
    | 回傳值: 無
    |
     */
    public function index($page = 0)
    {

        // 取得並設定頁面搜尋條件($page=0 時清空之前條件)
        // 排序條件:     $this->query['by']      = array('xxx'=>'DESC')
        // WHERE 條件:  $this->query['where']   = array('aaa'=>'a', 'bbb'=>'b')
        // 搜尋關鍵字:   $this->query['keyword'] = 'ccc'

        $this->set_query($page);

        // 重新設定頁碼
        $page = (empty($page)) ? 1 : $page;

        // 每頁數量
        $page_amount = 50;

        // 資料總數
        $data_amount = $this->T_user
            ->like('account', 'AND', $this->query['keyword'])
            ->num_rows($this->query['where'], 'id');

        // 頁面資料內容
        $this->data = $this->T_user
            ->like('account', 'AND', $this->query['keyword'])
            ->by('id', 'DESC')
            ->by($this->query['by'])
            ->limit($page_amount, $page_amount * ($page - 1))
            ->getAll('*', $this->query['where']);

        // 分頁列表(頁面顯示筆數, 總筆數, 頁碼)
        // $this->page_list = $this->create_page_list($page_amount, $data_amount, $page);

        // 指定View
        // $this->display('demo/index');
    }

    /*
    |--------------------------------------------------------------------------
    | 取得並設定頁面搜尋條件
    |--------------------------------------------------------------------------
    |
    | 呼叫方式: $this->set_query($page)
    | 參數:    $page: 目前頁面頁碼
    | 回傳值:  無
    | 說明: $page=0 且無設定任何條件時時清空之前條件
    |
     */
    private function set_query($page = 0)
    {
        // 初始化
        $this->query['by'] = array();
        $this->query['where'] = array();
        $this->query['keyword'] = '';
        $by_session = array();
        $where_session = array();
        $keyword_session = '';

        // query_mode: by(排序) / where / keyword
        $query_mode = $this->input->post('query_mode', true);

        // 新條件
        if (!empty($_POST)) {
            if ($query_mode == 'keyword') {
                foreach ($_POST as $k => $v) {
                    if ($k != 'query_mode') {
                        $this->query[$query_mode] = $this->input->post($k, true);
                    }
                }
            } else {
                foreach ($_POST as $k => $v) {
                    if ($k != 'query_mode') {
                        $this->query[$query_mode][$k] = $this->input->post($k, true);
                    }
                }
            }
        }

        // 取回舊條件
        $query_session = $this->session->userdata('query');

        if (!empty($query_session)) {
            $by_session = (empty($query_session['by'])) ? array() : $query_session['by'];
            $where_session = (empty($query_session['where'])) ? array() : $query_session['where'];
            $keyword_session = (empty($query_session['keyword'])) ? '' : $query_session['keyword'];
        }

        // 合併新舊條件
        if (!empty($by_session)) {
            foreach ($by_session as $k => $v) {
                if (empty($this->query['by'][$k])) {
                    $this->query['by'][$k] = $by_session[$k];
                }
            }
        }

        if (!empty($where_session)) {
            foreach ($where_session as $k => $v) {
                if (empty($this->query['where'][$k])) {
                    $this->query['where'][$k] = $where_session[$k];
                }
            }
        }

        if (!empty($keyword_session) && empty($this->query['keyword'])) {
            $this->query['keyword'] = $keyword_session;
        }

        // 寫回SESSION
        $this->session->set_userdata('query', $this->query);

        // $page=0 且無 query_mode 時, 清空搜尋條件/SESSION
        if (empty($page) && empty($query_mode)) {
            if (!empty($query_session)) {
                $this->session->unset_userdata('query');
            }

            $this->query['by'] = array();
            $this->query['where'] = array();
            $this->query['keyword'] = '';
        }
    }
}
