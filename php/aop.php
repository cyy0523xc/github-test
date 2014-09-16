<?php
/**
 * 使用PHP近似实现AOP
 * @author cyy0523xc@gmail.com
 */

/** 
 * 基类
 * @author cyy0523xc@gmail.com
 */
class CyyBase
{
    public function before()
    {
        echo "before\n";
    }

    public function after()
    {
        echo "after\n";
    }
}

/** 
 * 业务类
 * @author cyy0523xc@gmail.com
 */
class CyyControl extends CyyBase
{
    public function foobar()
    {
        echo '业务逻辑', "\n";
    }

    public function before()
    {
        parent::before();
        echo "child class before\n";
    }
}


/** 
 * 业务逻辑类的包装类
 * @author cyy0523xc@gmail.com
 */
class AOP
{
    private $instance;

    public function __construct($instance)
    {
        $this->instance = $instance;
    }

    public function __call($method, $params)
    {
        if (!$this->methodExists($method)) {
            throw new Exception("Call undefinded method " . get_class($this->instance) . "::$method");
        }

        // 调用前置函数
        if ($this->methodExists('before')) {
            $this->callMethod('before');
        }

        // 调用业务函数
        $return = $this->callMethod($method, $params);

        // 调用后置函数
        if ($this->methodExists('after')) {
            $this->callMethod('after');
        }
        
        return $return;
    }

    private function methodExists($method)
    {
        return method_exists($this->instance, $method);
    }

    private function callMethod($method, array $params = array())
    {
        $callBack = array(
            $this->instance,
            $method
        );
        return call_user_func_array($callBack, $params);
    }
}

/** 
 * 工厂方法
 *
 */
class Factory
{
    public function getInstance($class_name)
    {
        return new AOP(new $class_name());
    }
}

//客户端调用演示
try {
    $obj = Factory::getInstance('CyyControl');
    $obj->foobar();
} catch(Exception $e) {
    echo 'Caught exception: ', $e->getMessage();
}
